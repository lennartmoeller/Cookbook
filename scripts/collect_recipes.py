from helpers.collect_recipes import collect_recipes
from helpers.load_json import load_json
from helpers.save_json import save_json
from helpers.update_recipes import update_recipes


def main() -> None:
    fs_recipes = collect_recipes("recipes")
    current = load_json("recipes.json")
    updated = update_recipes(fs_recipes, current)
    save_json(updated, "recipes.json")
    print(f"recipes.json updated with {len(updated)} recipes.")

if __name__ == "__main__":
    main()
