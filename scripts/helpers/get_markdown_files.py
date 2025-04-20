from pathlib import Path


def get_markdown_files(directory: str | Path) -> list[Path]:
    base = Path(directory)
    return [
        f for f in base.rglob("*.md")
        if f.is_file() and not f.name.lower().endswith(".formatted.md")
    ]
