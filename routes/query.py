from fastapi import APIRouter
from pydantic import BaseModel
from utils.ai import ask_gemini
from utils.detector import get_system_info

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    error_context: str | None = None

@router.post("/query")
async def handle_query(req: QueryRequest):
    system_info = get_system_info()
    result = await ask_gemini(req.query, system_info, req.error_context)
    return result