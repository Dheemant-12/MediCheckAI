from fastapi import APIRouter

from app.services.ai_service import (
    analyze_symptoms
)

router = APIRouter()

@router.post("/analyze")
def analyze(data: dict):

    symptoms = data.get("symptoms")

    ai_response = analyze_symptoms(
        symptoms
    )

    return {
        "analysis": ai_response
    }