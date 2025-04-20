from helpers import collect_recipes, load_json, save_json, update_recipes


def main() -> None:
    fs_recipes = collect_recipes("recipes")
    current = load_json("recipes.json")
    updated = update_recipes(fs_recipes, current)
    save_json(updated, "recipes.json")
    print(f"recipes.json updated with {len(updated)} recipes.")

if __name__ == "__main__":
    main()
