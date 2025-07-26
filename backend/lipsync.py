# backend/lipsync.py
import subprocess
import os
from phonemizer import phonemize

class LipSync:
    """
    Wav2Lip wrapper with phoneme extraction.
    """
    def __init__(self, model_dir: str = 'models/lipsync/Wav2Lip'):
        self.checkpoint = os.path.join(model_dir, 'wav2lip.pth')
        self.script = os.path.join(model_dir, 'inference.py')

    def sync(self, video_path: str, audio_path: str, output_path: str) -> str:
        subprocess.run([
            'python3', self.script,
            '--checkpoint', self.checkpoint,
            '--face', video_path,
            '--audio', audio_path,
            '--outfile', output_path
        ], check=True)
        return output_path

    def extract_visemes(self, audio_path: str, text: str) -> list:
        phonemes = phonemize(
            text,
            language='en-us',
            backend='espeak',
            strip=True,
            preserve_punctuation=False
        )
        return phonemes.split()
