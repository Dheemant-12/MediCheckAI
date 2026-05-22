from fastapi import FastAPI
from app.routes.symptoms import router as symptoms_router
from app.routes.users import router as users_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "MediCheck AI Backend Running"}

app.include_router(symptoms_router)
app.include_router(users_router)