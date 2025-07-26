# backend/audio.py
import ffmpeg
import librosa
import numpy as np

class AudioManager:
    """
    Background music mixing, BPM sync, ducking, and panning.
    """
    def mix_music(
        self,
        speech_path: str,
        music_path: str,
        output_path: str,
        pan: float = 0.5,
        ducking: bool = True,
        loop: bool = True
    ) -> str:
        # Load speech and lower-volume music
        speech = ffmpeg.input(speech_path).audio
        music = ffmpeg.input(music_path).audio.filter('volume', 0.2)

        # Loop music if shorter than speech
        if loop:
            music = music.filter('aloop', loop=-1, size=2**32)

        # Duck music under speech
        if ducking:
            music = music.filter('sidechaincompress', threshold=-40, ratio=4)

        # Stereo panning
        music = music.filter('pan', f'stereo|c0={(1-pan)}*c0|c1={pan}*c1')

        # Output combined audio
        ffmpeg.output(speech, music, output_path, vcodec='copy', acodec='aac') \
            .overwrite_output().run(quiet=True)
        return output_path

    def detect_beats(self, audio_path: str):
        # Return tempo and beat timestamps
        y, sr = librosa.load(audio_path, sr=None)
        tempo, frames = librosa.beat.beat_track(y=y, sr=sr)
        times = librosa.frames_to_time(frames, sr=sr)
        return tempo, times
