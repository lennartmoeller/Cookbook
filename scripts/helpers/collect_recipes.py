from pathlib import Path

from get_markdown_files import get_markdown_files


def collect_recipes(directory: str) -> list[dict[str, str]]:
    recipes: list[dict[str, str]] = []
    for md_file in get_markdown_files(directory):
        rel_path = Path(md_file).relative_to(directory)
        parts = rel_path.parts
        category = parts[0] if len(parts) > 1 else ""
        name = md_file.stem
        recipes.append({"name": name, "category": category})
    return recipes
