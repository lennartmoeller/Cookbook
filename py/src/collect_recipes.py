from util.constants import RECIPES_DIR, RECIPES_JSON
from util.index_recipes import index_recipes
from util.load_json import load_json
from util.save_json import save_json
from util.update_recipes import update_recipes


def main() -> None:
    collected_recipes = index_recipes(RECIPES_DIR)
    json_contents = load_json(RECIPES_JSON)
    updated = update_recipes(collected_recipes, json_contents)
    save_json(updated, RECIPES_JSON)
    print(f"{RECIPES_JSON} updated with {len(updated)} recipes.")

if __name__ == "__main__":
    main()
