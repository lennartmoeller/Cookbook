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
