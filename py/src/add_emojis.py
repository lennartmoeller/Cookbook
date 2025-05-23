import json
import os

from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam
from pydantic import BaseModel

from util.constants import RECIPES_DIR, RECIPES_JSON
from util.index_recipes import index_recipes
from util.load_json import load_json
from util.save_json import save_json
from util.update_recipes import update_recipes

OpenAI.api_key = os.environ["OPENAI_API_KEY"]

class EmojiMapping(BaseModel):
    name: str
    category: str
    emoji: str

class EmojiResponse(BaseModel):
    recipes: list[EmojiMapping]

def get_emojis(recipes: list[dict[str, str]]) -> dict[tuple[str, str], str]:
    prompt = (
        "You will be given a list of recipes in JSON format. Each recipe has a 'name' and a 'category'. "
        "For each recipe, decide how many emojis (between 1 and 3) are necessary to represent the recipe without adding unnecessary ones. "
        "Return the result as valid JSON with a key 'recipes' mapping to an array of objects, "
        "each object having 'name', 'category', and 'emoji' keys, where 'emoji' is a string concatenating the necessary emojis without spaces. "
        "Only output the JSON without any additional text.\n\nList of recipes:\n" + json.dumps(recipes)
    )
    client = OpenAI()
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[ChatCompletionUserMessageParam(content=prompt, role="user")],
        response_format=EmojiResponse,
    )
    message = response.choices[0].message.parsed
    return {(m.name, m.category): m.emoji for m in message.recipes}

def main() -> None:
    fs_recipes = index_recipes(RECIPES_DIR)
    current = load_json(RECIPES_JSON)
    updated = update_recipes(fs_recipes, current)
    missing = [r for r in updated if not r.get("emoji")]
    if missing:
        emojis = get_emojis(missing)
        for r in updated:
            key = (r["name"], r["category"])
            if not r.get("emoji") and key in emojis:
                r["emoji"] = emojis[key]
    save_json(updated, RECIPES_JSON)
    print("recipes.json updated with emojis.")

if __name__ == "__main__":
    main()
