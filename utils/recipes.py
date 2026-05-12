import os
import yaml
from rapidfuzz import fuzz

RECIPES_DIR = os.path.join(os.path.dirname(__file__), '..', 'recipes')
MATCH_THRESHOLD = 75

def load_recipes() -> list[dict]:
    recipes = []
    for fname in os.listdir(RECIPES_DIR):
        if fname.endswith('.yaml'):
            with open(os.path.join(RECIPES_DIR, fname)) as f:
                recipes.append(yaml.safe_load(f))
    return recipes

def find_recipe(query: str) -> dict | None:
    query = query.strip().lower()
    recipes = load_recipes()

    best_score = 0
    best_recipe = None

    for recipe in recipes:
        for trigger in recipe.get('triggers', []):
            score = fuzz.ratio(query, trigger.lower())
            if score > best_score:
                best_score = score
                best_recipe = recipe

    if best_score >= MATCH_THRESHOLD:
        return best_recipe
    return None

def recipe_to_response(recipe: dict) -> dict:
    return {
        "summary": recipe['summary'],
        "steps": recipe['steps'],
        "source": "official",
        "warning": f"Source: {recipe['url']}" if recipe.get('url') else None,
    }