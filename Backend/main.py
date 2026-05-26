from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.symptoms import router as symptoms_router
from app.routes.users import router as users_router

from app.database.connection import engine, Base

from app.models.user_model import User
from app.models.symptom_model import SymptomLog

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "MediCheck AI Backend Running"
    }

app.include_router(symptoms_router)

app.include_router(users_router)