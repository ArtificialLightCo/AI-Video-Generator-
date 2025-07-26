# backend/stt.py
import whisper
import os

class SpeechToText:
    """
    Whisper-based speech-to-text transcription.
    """
    def __init__(self, model_name: str = 'small'):
        # loads and caches the Whisper model
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: str, language: str = 'en') -> str:
        """
        Transcribe an audio file; returns the text.
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f\"Audio file not found: {audio_path}\")
        result = self.model.transcribe(audio_path, language=language)
        return result.get('text', '').strip()
