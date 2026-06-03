from fastapi import APIRouter, Depends

from app.services.ai_service_nvidia import (
    analyze_symptoms
)

from app.database.connection import SessionLocal

from app.models.chat_model import ChatHistory

from app.security.current_user import (
    get_current_user
)

router = APIRouter()

@router.post("/analyze")
def analyze(
    data: dict,
    current_user = Depends(
        get_current_user
    )
):

    symptoms = data.get(
        "symptoms"
    )

    session_id = data.get(
        "session_id"
    )
    print("SESSION ID RECEIVED:",session_id)

    response = analyze_symptoms(
        symptoms
    )

    db = SessionLocal()

    chat = ChatHistory(
        user_id=current_user.id,
        session_id=session_id,
        user_message=symptoms,
        ai_response=response
    )

    db.add(chat)

    db.commit()

    db.refresh(chat)

    print(
        "SAVED CHAT SESSION ID:",
        chat.session_id
    )

    db.close()

    return {
        "analysis": response
    }