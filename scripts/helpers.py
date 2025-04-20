import json
import os
from pathlib import Path


def collect_recipes(directory: str) -> list[dict[str, str]]:
    recipes = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".md") and not file.lower().endswith(".formatted.md"):
                rel = os.path.relpath(root, directory)
                category = "" if rel == "." else Path(rel).parts[0]
                name = Path(file).stem
                recipes.append({"name": name, "category": category})
    return recipes

def load_json(path: str) -> list[dict[str, str]]:
    if Path(path).exists():
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(data: list[dict[str, str]], path: str) -> None:
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_recipes(fs_recipes: list[dict[str, str]], current: list[dict[str, str]]) -> list[dict[str, str]]:
    curr_map: dict[tuple[str, str], dict[str, str]] = {(r["name"], r["category"]): r for r in current}
    fs_keys = {(r["name"], r["category"]) for r in fs_recipes}
    for r in fs_recipes:
        key = (r["name"], r["category"])
        if key in curr_map:
            merged = curr_map[key].copy()
            merged.update(r)
            merged.setdefault("formatted", False)
            curr_map[key] = merged
        else:
            new_r = r.copy()
            new_r.setdefault("formatted", False)
            curr_map[key] = new_r
    return [curr_map[k] for k in curr_map if k in fs_keys]
