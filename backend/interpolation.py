# backend/interpolation.py
import os
import torch
from pathlib import Path
from PIL import Image
from torchvision.transforms.functional import to_tensor, to_pil_image
from einops import rearrange
from rife import RIFE  # assume a RIFE wrapper is installed

class Interpolator:
    """
    Frame interpolation using RIFE for smooth motion.
    """
    def __init__(self, model_path: str = 'models/interp/RIFE'):
        self.model = RIFE(model_path=model_path).to('cuda' if torch.cuda.is_available() else 'cpu')

    def interpolate(
        self,
        video_path: str,
        factor: int = 2,
        output_path: str = None
    ) -> str:
        # Extract frames
        temp_dir = Path(video_path).with_suffix('') / 'frames'
        temp_dir.mkdir(parents=True, exist_ok=True)
        (
            ffmpeg
            .input(video_path)
            .output(str(temp_dir / 'frame_%04d.png'))
            .overwrite_output()
            .run(quiet=True)
        )

        # Load and interpolate
        frame_files = sorted(temp_dir.glob('frame_*.png'))
        interp_frames = []
        for a, b in zip(frame_files, frame_files[1:]):
            img1 = to_tensor(Image.open(a)).unsqueeze(0).cuda()
            img2 = to_tensor(Image.open(b)).unsqueeze(0).cuda()
            interp_frames.append(img1)
            for i in range(1, factor):
                t = i / factor
                mid = self.model.infer(img1, img2, t)
                interp_frames.append(mid)
        interp_frames.append(to_tensor(Image.open(frame_files[-1])).unsqueeze(0).cuda())

        # Save interpolated video
        if output_path is None:
            output_path = video_path.replace('.mp4', f'_interp.mp4')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        writer = ffmpeg.input('pipe:', format='rawvideo', pix_fmt='rgb24',
                              s=f'{img1.shape[3]}x{img1.shape[2]}', framerate=30)
        writer = writer.output(
            output_path,
            vcodec='libx264',
            pix_fmt='yuv420p'
        ).overwrite_output().run_async(pipe_stdin=True)

        for frame in interp_frames:
            frame_np = rearrange(frame[0].cpu().numpy(), 'c h w -> h w c')
            writer.stdin.write((frame_np * 255).astype('uint8').tobytes())
        writer.stdin.close()
        writer.wait()

        # Cleanup
        for f in temp_dir.glob('*'): f.unlink()
        temp_dir.rmdir()
        return output_path
