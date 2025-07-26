# backend/tts.py
import os
import librosa
import numpy as np
from TTS.api import TTS as CoquiTTS

class TextToSpeech:
    """
    Coqui TTS with emotion control and independent pitch shifting.
    """
    def __init__(self,
                 model_name: str = 'tts_models/en/vctk/vits',
                 device: str = None):
        # Multi-speaker VITS supports cloning via speaker_wav
        self.tts = CoquiTTS(model_name=model_name, gpu=(device=='cuda'))

    def synthesize(
        self,
        text: str,
        output_path: str,
        speaker_wav: str = None,
        emotion: str = None,
        pitch_shift: float = 0.0
    ) -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # 1) Generate raw TTS
        wav_data = self.tts.tts(text=text, speaker_wav=speaker_wav)
        temp_path = output_path.replace('.wav', '_raw.wav')
        self.tts.save_wav(wav_data, temp_path)

        # 2) Load for post-processing
        y, sr = librosa.load(temp_path, sr=None)
        # Emotion-based speed
        speeds = {'happy': 1.2, 'sad': 0.8, 'angry': 1.1}
        if emotion in speeds:
            y = librosa.effects.time_stretch(y, speeds[emotion])
        # Independent pitch shift
        if pitch_shift != 0.0:
            y = librosa.effects.pitch_shift(y, sr, pitch_shift)
        # Trim silence
        y, _ = librosa.effects.trim(y)
        # 3) Save final WAV
        librosa.output.write_wav(output_path, y, sr)
        # Cleanup temp file
        os.remove(temp_path)
        return output_path
