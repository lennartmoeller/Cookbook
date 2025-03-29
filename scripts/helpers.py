import os
import json
from typing import List, Dict, Tuple

def collect_recipes(directory: str) -> List[Dict[str, str]]:
    recipes = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".md"):
                rel = os.path.relpath(root, directory)
                category = "" if rel == "." else rel.split(os.sep)[0]
                name, _ = os.path.splitext(file)
                recipes.append({"name": name, "category": category})
    return recipes

def load_json(path: str) -> List[Dict[str, str]]:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(data: List[Dict[str, str]], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_recipes(fs_recipes: List[Dict[str, str]], current: List[Dict[str, str]]) -> List[Dict[str, str]]:
    curr_map: Dict[Tuple[str, str], Dict[str, str]] = {(r["name"], r["category"]): r for r in current}
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
