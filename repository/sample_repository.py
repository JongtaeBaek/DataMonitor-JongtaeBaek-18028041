import json
from dataclasses import asdict
from pathlib import Path

from model.sample import Sample


class SampleRepository:
    def __init__(self, filepath: str = "data/samples.json"):
        self._path = Path(filepath)

    def load(self) -> list[Sample]:
        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as f:
            return [Sample(**item) for item in json.load(f)]

    def save(self, samples: list[Sample]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as f:
            json.dump([asdict(s) for s in samples], f, ensure_ascii=False, indent=2)
