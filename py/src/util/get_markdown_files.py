from pathlib import Path


def get_markdown_files(directory: str | Path, variant: str | None = None) -> list[Path]:
    base = Path(directory)
    files: list[Path] = []
    for f in base.rglob("*.md"):
        if not f.is_file():
            continue
        suffixes = [s.lower() for s in f.suffixes]
        if variant is None:
            if suffixes == [".md"]:
                files.append(f)
        else:
            target = f".{variant.lower()}"
            if len(suffixes) >= 2 and suffixes[-2] == target and suffixes[-1] == ".md":
                files.append(f)
    return files
