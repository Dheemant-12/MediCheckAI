from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.symptom_schema import (
    SymptomRequest,
    SymptomResponse
)

from app.models.symptom_model import SymptomLog

from app.database.dependencies import get_db

router = APIRouter()

@router.post("/analyze", response_model=SymptomResponse)
def analyze_symptoms(
    data: SymptomRequest,
    db: Session = Depends(get_db)
):

    urgency = "Low"

    if "chest pain" in data.symptoms.lower():
        urgency = "High"

    recommendation = "Consult a doctor if symptoms persist"

    symptom_entry = SymptomLog(
        symptoms=data.symptoms,
        urgency=urgency,
        recommendation=recommendation
    )

    db.add(symptom_entry)

    db.commit()

    db.refresh(symptom_entry)

    return {
        "symptoms": data.symptoms,
        "urgency": urgency,
        "recommendation": recommendation
    }