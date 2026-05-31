from fastapi import APIRouter
from app.services.ai_service_nvidia import analyze_symptoms

from app.database.connection import SessionLocal
from app.models.chat_model import ChatHistory

router = APIRouter()

@router.post("/analyze")
def analyze(data: dict):

    symptoms = data.get("symptoms")

    response = analyze_symptoms(symptoms)

    db = SessionLocal()

    chat = ChatHistory(
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