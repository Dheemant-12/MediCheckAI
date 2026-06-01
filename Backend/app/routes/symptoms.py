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

    symptoms = data.get("symptoms")

    response = analyze_symptoms(
        symptoms
    )

    db = SessionLocal()

    chat = ChatHistory(
        user_id=current_user.id,
        user_message=symptoms,
        ai_response=response
    )

    db.add(chat)

    db.commit()

    db.refresh(chat)

    db.close()

    return {
        "analysis": response
    }