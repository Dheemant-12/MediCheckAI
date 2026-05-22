from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_route():
    return {
        "message": "Symptoms route working"
    }

@router.post("/analyze")
def analyze_symptoms(data: dict):
    return {
        "received_symptoms": data,
        "status": "Analysis completed"
    }

@router.get("/user")
def get_user(name: str, age: int):
    return {
        "name": name,
        "age": age
    }