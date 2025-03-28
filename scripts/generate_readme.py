import os
import json
from collections import defaultdict
from typing import List, Dict

def generate_readme(recipes: List[Dict[str, str]]) -> str:
    groups = defaultdict(list)
    for r in recipes:
        if r.get("category") == "Rezeptschritte":
            continue
        groups[r.get("category", "")].append(r)
    lines = ["# Kochbuch", ""]
    for cat in sorted(groups.keys()):
        heading = f"## {cat}" if cat else "## Uncategorized"
        lines.append(heading)
        lines.append("")
        for r in sorted(groups[cat], key=lambda x: x["name"]):
            name = r["name"]
            emoji = r.get("emoji", "")
            display = f"{name} {emoji}" if emoji else name
            path = f"recipes/{cat}/{name}.md" if cat else f"recipes/{name}.md"
            lines.append(f"- [{display}](<{path}>)")
        lines.append("")
    return "\n".join(lines)

def main() -> None:
    with open("recipes.json", "r", encoding="utf-8") as f:
        recipes = json.load(f)
    readme = generate_readme(recipes)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print("README.md generated.")

if __name__ == "__main__":
    main()
