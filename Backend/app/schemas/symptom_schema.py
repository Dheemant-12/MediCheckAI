from pydantic import BaseModel, Field

class SymptomRequest(BaseModel):
    symptoms: str = Field(..., min_length=3, max_length=500)
    age: int = Field(..., gt=0, lt=120)
    gender: str
    duration_days: int = Field(..., gt=0, lt=365)
class SymptomResponse(BaseModel):
    symptoms: str
    urgency: str
    recommendation: str    
class UserSignup(BaseModel):

    username: str

    email: str

    password: str


class UserLogin(BaseModel):

    email: str

    password: str    