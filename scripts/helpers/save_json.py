import json
from pathlib import Path


def save_json(data: list[dict[str, str]], path: str) -> None:
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
