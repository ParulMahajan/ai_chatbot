from fastapi import APIRouter
from fastapi import Header
from request.req import ChatRequest
from service.doc_service import chat_response

router = APIRouter()

@router.post("/chat")
async def chat(chat_request: ChatRequest, user_id: str = Header()) -> str:

    result = await chat_response(chat_request.message, user_id)
    return result
