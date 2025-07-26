# backend/model_manager.py
import os
from pathlib import Path
from huggingface_hub import snapshot_download

class ModelManager:
    """
    Download and cache model repositories from Hugging Face Hub.
    """
    def __init__(self, cache_dir='models'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download(self, repo_id: str) -> str:
        """
        Clone or retrieve a model repo by ID. Returns local path.
        """
        # snapshot_download will reuse cache if already present
        local_path = snapshot_download(
            repo_id=repo_id,
            cache_dir=str(self.cache_dir)
        )
        return local_path
