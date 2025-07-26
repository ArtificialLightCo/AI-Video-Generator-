# backend/orchestration.py

import os
from backend.pipelines import VideoPipeline
from backend.tts import TextToSpeech
from backend.lipsync import LipSync
from backend.audio import AudioManager
from backend.styles import StyleManager
from backend.interpolation import Interpolator
from backend.stitch import Stitcher

class Orchestrator:
    """
    Top-level orchestrator: splits prompt into scenes,
    generates video+audio, applies lip-sync, interpolation,
    music mixing, stitching, and VFX overlays.
    """

    def __init__(self):
        self.pipeline     = VideoPipeline()
        self.tts          = TextToSpeech()
        self.lipsync      = LipSync()
        self.audio_mgr    = AudioManager()
        self.styler       = StyleManager()
        self.interpolator = Interpolator()
        self.stitcher     = Stitcher()
        self.fps          = 8  # base FPS

    def create_video(
        self,
        prompt: str,
        total_duration: int,
        output_path: str,
        scene_delimiter: str = '|',
        style: str = None,
        music_path: str = None,
        interpolate_factor: int = 1,
        init_image: str = None,
        particles: bool = False,
        title_text: str = None,
        camera_shake: bool = False
    ) -> str:
        # 1) Split into scenes
        scenes = [s.strip() for s in prompt.split(scene_delimiter)]
        num_scenes = len(scenes)
        per = total_duration // num_scenes

        # 2) Generate each segment
        seg_paths = []
        for i, scene in enumerate(scenes):
            seg = f'outputs/segments/seg_{i}.mp4'
            self.pipeline.generate_segment(
                scene,
                num_frames=per * self.fps,
                fps=self.fps,
                output_path=seg,
                init_image=init_image
            )
            # 2a) Optional interpolation
            if interpolate_factor > 1:
                interp_out = seg.replace('.mp4', f'_interp.mp4')
                self.interpolator.interpolate(
                    seg,
                    factor=interpolate_factor,
                    output_path=interp_out
                )
                seg = interp_out
            seg_paths.append(seg)

        # 3) Synthesize speech for full prompt
        audio_path = f'outputs/audio/speech.wav'
        os.makedirs(os.path.dirname(audio_path), exist_ok=True)
        self.tts.synthesize(prompt, audio_path)

        # 4) Apply lip-sync to each segment
        synced = []
        for seg in seg_paths:
            out = seg.replace('.mp4', '_synced.mp4')
            self.lipsync.sync(seg, audio_path, out)
            synced.append(out)

        # 5) Mix background music if provided
        main_audio = audio_path
        if music_path:
            mixed = audio_path.replace('.wav', '_mixed.mp3')
            self.audio_mgr.mix_music(
                speech_path=audio_path,
                music_path=music_path,
                output_path=mixed
            )
            main_audio = mixed

        # 6) Stitch segments together
        stitched = self.stitcher.stitch_segments(
            video_paths=synced,
            audio_path=main_audio,
            output_path=output_path
        )

        # 7) Apply style + VFX overlays
        final = stitched
        if style:
            final = self.styler.apply_lut(final, style)
        if particles:
            final = self.styler.overlay_particles(
                final,
                final.replace('.mp4', '_particles.mp4'),
                'assets/confetti.mp4'
            )
        if title_text:
            final = self.styler.add_animated_title(
                final,
                final.replace('.mp4', '_title.mp4'),
                text=title_text
            )
        if camera_shake:
            final = self.styler.camera_shake(
                final,
                final.replace('.mp4', '_shake.mp4')
            )

        return final
