from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user_model import User

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )

    email = payload.get("sub")

    user = db.query(User).filter(
        User.email == email
    ).first()

    return user