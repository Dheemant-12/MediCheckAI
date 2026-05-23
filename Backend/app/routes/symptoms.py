from fastapi import APIRouter
from app.schemas.symptom_schema import SymptomRequest, SymptomResponse

router = APIRouter()

@router.get("/test")
def test_route():
    return {
        "message": "Symptoms route working"
    }

@router.post("/analyze", response_model=SymptomResponse)
def analyze_symptoms(data: SymptomRequest):

    urgency = "Low"

    if "chest pain" in data.symptoms.lower():
        urgency = "High"

    return {
        "symptoms": data.symptoms,
        "urgency": urgency,
        "recommendation": "Consult a doctor if symptoms persist"
    }