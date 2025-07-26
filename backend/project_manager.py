# backend/project_manager.py
import json
import time
from pathlib import Path

class ProjectManager:
    """
    Save, load, and version project states with timestamped versions.
    """
    def __init__(self, dir='projects'):
        self.dir = Path(dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    def list_projects(self) -> list:
        """
        List all project names.
        """
        return [p.name for p in self.dir.iterdir() if p.is_dir()]

    def list_versions(self, name: str) -> list:
        """
        List versions (timestamps) for a project.
        """
        proj = self.dir / name
        if not proj.exists():
            return []
        return sorted([f.stem for f in proj.glob('*.json')])

    def save(self, name: str, data: dict) -> str:
        """
        Save a new version of the project state as timestamp.json.
        """
        proj = self.dir / name
        proj.mkdir(parents=True, exist_ok=True)
        ts = time.strftime('%Y%m%d_%H%M%S')
        path = proj / f"{ts}.json"
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        return str(path)

    def load(self, name: str, version: str = None) -> dict:
        """
        Load a project version; default to latest if version is None.
        """
        proj = self.dir / name
        if not proj.exists():
            raise FileNotFoundError(f"Project {name} not found")
        versions = self.list_versions(name)
        if not versions:
            raise FileNotFoundError(f"No versions for project {name}")
        ver = version or versions[-1]
        path = proj / f"{ver}.json"
        with open(path) as f:
            return json.load(f)
