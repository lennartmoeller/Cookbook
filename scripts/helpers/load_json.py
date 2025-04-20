import json
from pathlib import Path


def load_json(path: str) -> list[dict[str, str]]:
    if Path(path).exists():
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f)
    return []
