from fastapi import APIRouter

from app.database.connection import SessionLocal
from app.models.chat_model import ChatHistory

router = APIRouter()

@router.get("/history")
def get_history():

    db = SessionLocal()

    chats = db.query(
        ChatHistory
    ).all()

    db.close()

    result = []

    for chat in chats:

        result.append({
            "user_message":
                chat.user_message,
            "ai_response":
                chat.ai_response
        })

    return result