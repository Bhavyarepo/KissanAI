import json
import os
import zipfile
from pathlib import Path
from typing import Optional

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

class KaggleDatasetManager:
    def __init__(self, datasets_dir: str = "datasets"):
        self.datasets_dir = datasets_dir
        ensure_dir(self.datasets_dir)

    def _has_kaggle_creds(self) -> bool:
        # Either ~/.kaggle/kaggle.json exists or env vars are set
        kaggle_home = Path.home() / ".kaggle" / "kaggle.json"
        return kaggle_home.exists() or (
            os.getenv("KAGGLE_USERNAME") and os.getenv("KAGGLE_KEY")
        )

    def _install_kaggle_creds_from_env(self):
        kaggle_home = Path.home() / ".kaggle"
        kaggle_home.mkdir(parents=True, exist_ok=True)
        kaggle_json = kaggle_home / "kaggle.json"
        if not kaggle_json.exists():
            username = os.getenv("KAGGLE_USERNAME")
            key = os.getenv("KAGGLE_KEY")
            if username and key:
                # Create a Python dictionary with the credentials
                credentials = {"username": username, "key": key}

# Open the file in write mode and use json.dump() to write the dictionary
                with open(kaggle_json, 'w') as f:
                    json.dump(credentials, f, indent=2)
                
                os.chmod(str(kaggle_json), 0o600)

    def download_if_missing(self, dataset_slug: str, target_subdir: str) -> str:
        """
        dataset_slug: e.g. "arjunyadav99/indian-agricultural-mandi-prices-20232025"
        target_subdir: folder name under datasets/
        returns local dataset folder path
        """
        from kaggle.api.kaggle_api_extended import KaggleApi

        target_dir = Path(self.datasets_dir) / target_subdir
        ensure_dir(str(target_dir))

        # Heuristic: if directory has files, assume present
        if any(target_dir.iterdir()):
            return str(target_dir)

        if not self._has_kaggle_creds():
            self._install_kaggle_creds_from_env()

        api = KaggleApi()
        api.authenticate()

        api.dataset_download_files(dataset_slug, path=str(target_dir), unzip=True, quiet=False)
        return str(target_dir)






