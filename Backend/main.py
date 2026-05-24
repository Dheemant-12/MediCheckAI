from fastapi import FastAPI

from app.routes.symptoms import router as symptoms_router
from app.routes.users import router as users_router

from app.database.connection import engine, Base

from app.models.user_model import User
from app.models.symptom_model import SymptomLog

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "MediCheck AI Backend Running"
    }

app.include_router(symptoms_router)

app.include_router(users_router)