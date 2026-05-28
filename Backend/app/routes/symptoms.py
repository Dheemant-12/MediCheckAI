from fastapi import APIRouter

from app.services.ai_service_nvidia import (
    analyze_symptoms
)

router = APIRouter()

@router.post("/analyze")

def analyze(data: dict):

    symptoms = data.get("symptoms")

    response = analyze_symptoms(
        symptoms
    )

    return {
        "analysis": response
    }