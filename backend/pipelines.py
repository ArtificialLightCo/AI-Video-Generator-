# backend/pipelines.py
import os
import tempfile
import torch
from diffusers import DiffusionPipeline
import ffmpeg
from transformers import logging as hf_logging

hf_logging.set_verbosity_error()

class VideoPipeline:
    """
    Unified text-to-video pipeline with ModelScope primary
    and Stable Video Diffusion fallback.
    """
    def __init__(
        self,
        primary_model: str = 'damo-vilab/modelscope-text-to-video-synthesis',
        fallback_model: str = 'stabilityai/stable-video-diffusion-img2vid-xt',
        device: str = None
    ):
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        torch_dtype = torch.float16 if self.device == 'cuda' else torch.float32
        try:
            self.pipe = DiffusionPipeline.from_pretrained(
                primary_model, torch_dtype=torch_dtype
            ).to(self.device)
        except Exception:
            self.pipe = DiffusionPipeline.from_pretrained(
                fallback_model, torch_dtype=torch_dtype
            ).to(self.device)

    def generate_segment(
        self,
        prompt: str,
        num_frames: int = 32,
        height: int = 512,
        width: int = 512,
        fps: int = 8,
        output_path: str = None
    ) -> str:
        tmpdir = tempfile.mkdtemp(prefix='vidseg_')
        pattern = os.path.join(tmpdir, 'frame_%04d.png')
        for i in range(num_frames):
            out = self.pipe(
                prompt,
                height=height,
                width=width,
                num_inference_steps=25
            )
            img = out.images[0]
            img.save(pattern % i)
        if output_path:
            (
                ffmpeg
                .input(os.path.join(tmpdir, 'frame_%04d.png'), framerate=fps)
                .output(output_path, vcodec='libx264', crf=18)
                .overwrite_output()
                .run(quiet=True)
            )
            # cleanup
            for f in os.listdir(tmpdir):
                os.remove(os.path.join(tmpdir, f))
            os.rmdir(tmpdir)
            return output_path
        return tmpdir
