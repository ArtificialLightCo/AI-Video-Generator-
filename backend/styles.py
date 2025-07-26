# backend/styles.py
import ffmpeg
import random

class StyleManager:
    """
    Applies LUTs, VFX overlays (particles, titles), and camera shake.
    """
    def apply_lut(self, input_path: str, lut_path: str) -> str:
        output = input_path.replace('.mp4', '_styled.mp4')
        ffmpeg.input(input_path).output(
            output,
            vf=f"lut3d='{lut_path}'"
        ).overwrite_output().run(quiet=True)
        return output

    def overlay_particles(self, input_path: str, output_path: str, particle_video: str) -> str:
        # Overlay a looping transparent particle video (e.g., confetti)
        ffmpeg.input(input_path).overlay(
            ffmpeg.input(particle_video).filter('loop', loop=-1, size=9999)
        ).output(output_path, vcodec='libx264', acodec='aac').overwrite_output().run(quiet=True)
        return output_path

    def add_animated_title(self, input_path: str, output_path: str, text: str, duration: int = 3) -> str:
        # Create animated title clip
        title_clip = (
            ffmpeg
            .input('color=c=black:s=1920x1080:d=' + str(duration), f='lavfi')
            .drawtext(
                text=text,
                fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                fontsize=72,
                fontcolor='white',
                x='(w-text_w)/2',
                y='(h-text_h)/2',
                enable=f'between(t,0,{duration})',
                alpha=f"if(lt(t,0.5),t*2,if(lt(t,{duration}-0.5),(1-(t-{duration}+0.5)*2),0))"
            )
        )
        # Concatenate title + main video
        ffmpeg.concat(title_clip, ffmpeg.input(input_path), v=1, a=1).output(
            output_path,
            vcodec='libx264',
            acodec='aac'
        ).overwrite_output().run(quiet=True)
        return output_path

    def camera_shake(self, input_path: str, output_path: str, intensity: float = 5.0) -> str:
        # Apply a slight shake effect by shifting frames randomly
        cmd = (
            ffmpeg
            .input(input_path)
            .filter('geq',
                r=f"p(X+random(0)*{intensity},Y)",
                g=f"p(X,Y+random(1)*{intensity},8)",
                b=f"p(X,Y,8)"
            )
            .output(output_path, vcodec='libx264', acodec='copy')
            .overwrite_output()
        )
        cmd.run(quiet=True)
        return output_path
