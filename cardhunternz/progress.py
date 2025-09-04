# progress.py
import json
from pathlib import Path

class ProgressTracker:
    def __init__(self, file_path: str = "scrape_progress.json"):
        self.file_path = Path(file_path)
        self.data = {}
        self.load()

    def load(self):
        if self.file_path.exists():
            with self.file_path.open("r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save(self):
        with self.file_path.open("w") as f:
            json.dump(self.data, f, indent=2)

    def get(self, store_name: str, key: str, default=None):
        return self.data.get(store_name, {}).get(key, default)

    def set(self, store_name: str, key: str, value):
        if store_name not in self.data:
            self.data[store_name] = {}
        self.data[store_name][key] = value
        self.save()
