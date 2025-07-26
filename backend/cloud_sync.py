# backend/cloud_sync.py
import subprocess
import os
from typing import List

class CloudSync:
    """
    Sync directories to cloud storage via rclone, with listing support.
    """
    def __init__(self, remote='drive'):
        self.remote = remote

    def list_remote(self) -> List[str]:
        """
        List top-level directories/files in the remote.
        """
        result = subprocess.run(
            ['rclone', 'lsf', f"{self.remote}:/"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().splitlines()

    def upload(self, local: str, remote_path: str) -> bool:
        """
        Upload local directory to remote:remote_path.
        """
        if not os.path.exists(local):
            raise FileNotFoundError(f"Local path {local} does not exist")
        subprocess.run(['rclone', 'copy', local, f"{self.remote}:{remote_path}"], check=True)
        return True

    def download(self, remote_path: str, local: str) -> bool:
        """
        Download remote:remote_path to local directory.
        """
        os.makedirs(local, exist_ok=True)
        subprocess.run(['rclone', 'copy', f"{self.remote}:{remote_path}", local], check=True)
        return True
