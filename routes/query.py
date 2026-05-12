from fastapi import APIRouter
from pydantic import BaseModel
from utils.ai import ask_gemini
from utils.detector import get_system_info
from utils.recipes import find_recipe, recipe_to_response
from utils import cache

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    error_context: str | None = None

@router.post("/query")
async def handle_query(req: QueryRequest):
    # 1. Check recipes first (no AI, no cache needed)
    if not req.error_context:
        recipe = find_recipe(req.query)
        if recipe:
            return {**recipe_to_response(recipe), "provider": "recipe"}

    # 2. Check cache
    cached = cache.get(req.query, req.error_context)
    if cached:
        return {**cached, "provider": "cache"}

    # 3. Fall back to Gemini
    system_info = get_system_info()
    result, provider = await ask_gemini(req.query, system_info, req.error_context)

    if result.get('steps'):
        cache.set(req.query, result, req.error_context)

    return {**result, "provider": provider}