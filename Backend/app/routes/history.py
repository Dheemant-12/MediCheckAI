from fastapi import APIRouter, Depends

from app.database.connection import SessionLocal

from app.models.chat_model import ChatHistory

from app.security.current_user import (
    get_current_user
)

router = APIRouter()


@router.get("/history")
def get_history(
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    chats = db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user.id
    ).all()

    result = []

    for chat in chats:

        result.append({
            "user_message":
                chat.user_message,
            "ai_response":
                chat.ai_response
        })

    db.close()

    return result


@router.get("/session/{session_id}/history")
def get_session_history(
    session_id: int,
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    chats = db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user.id,
        ChatHistory.session_id ==
        session_id
    ).all()

    result = []

    for chat in chats:

        result.append({
            "user_message":
                chat.user_message,
            "ai_response":
                chat.ai_response
        })

    db.close()

    return result


@router.delete("/history")
def clear_history(
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user.id
    ).delete()

    db.commit()

    db.close()

    return {
        "message":
        "History cleared successfully"
    }