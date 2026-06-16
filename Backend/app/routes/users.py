from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session
from jose import jwt

from app.database.dependencies import get_db

from app.models.user_model import User
from app.models.chat_model import ChatHistory
from app.models.chat_session_model import ChatSession
from sqlalchemy import func
from collections import Counter

from app.security.current_user import (
    get_current_user
)
from app.schemas.symptom_schema import UserSignup

from app.security.auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()

@router.post("/signup")
def signup(
    user: UserSignup,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        return {
            "error": "Email already exists"
        }

    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pw
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not existing_user:

        return {
            "access_token": "",
            "token_type": "bearer",
            "message": "Invalid email"
        }

    valid_password = verify_password(
        form_data.password,
        existing_user.password
    )

    if not valid_password:

        return {
            "access_token": "",
            "token_type": "bearer",
            "message": "Invalid password"
        }

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile")
def profile(
    current_user = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    )
):

    total_sessions = db.query(
        ChatSession
    ).filter(
        ChatSession.user_id ==
        current_user.id
    ).count()

    total_messages = db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user.id
    ).count()
    average_messages = 0

    if total_sessions > 0:

        average_messages = round(
            total_messages /
            total_sessions,
            2
        )
    most_active = db.query(

        ChatHistory.session_id,

        func.count(
            ChatHistory.id
        ).label(
            "message_count"
        )

    ).filter(

        ChatHistory.user_id ==
        current_user.id

    ).group_by(

        ChatHistory.session_id

    ).order_by(

        func.count(
            ChatHistory.id
        ).desc()

    ).first()     
    most_active_title =(
        "No Conversations"
    )
    if most_active:

        session = db.query(
            ChatSession
        ).filter(
            ChatSession.id ==
            most_active.session_id
        ).first()

        if session:

            most_active_title =(
                session.title   
            )
    return {

        "email":
        current_user.email,

        "username":
        current_user.username,

        "total_sessions":
        total_sessions,

        "total_messages":
        total_messages,

        "average_messages":
        average_messages,

        "most_active":
        most_active_title

    }
@router.get("/timeline")
def timeline(

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    sessions = db.query(
        ChatSession
    ).filter(

        ChatSession.user_id ==
        current_user.id

    ).order_by(

        ChatSession.id.desc()

    ).all()

    result = []

    for session in sessions:

        result.append({

            "id":
            session.id,

            "title":
            session.title

        })

    return result
@router.get("/symptom-trends")
def symptom_trends(

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    sessions = db.query(
        ChatSession
    ).filter(
        ChatSession.user_id ==
        current_user.id
    ).all()

    words = []

    for session in sessions:

        title_words = (
            session.title
            .lower()
            .split()
        )

        for word in title_words:

            if len(word) > 2:

                words.append(
                    word
                )

    counter = Counter(
        words
    )

    result = []

    for word, count in counter.most_common(5):

        result.append({

            "symptom": word,

            "count": count

        })

    return result
@router.get("/health-insights")
def health_insights(

    current_user = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    )

):

    sessions = db.query(
        ChatSession
    ).filter(
        ChatSession.user_id ==
        current_user.id
    ).all()

    words = []

    stop_words = [

        "and",
        "the",
        "for",
        "with",
        "issues",
        "discussion"

    ]

    for session in sessions:

        title_words = (
            session.title
            .lower()
            .split()
        )

        for word in title_words:

            if (
                len(word) > 2
                and word not in stop_words
            ):

                words.append(
                    word
                )

    counter = Counter(
        words
    )

    insights = []

    for word, count in counter.most_common(3):

        if count > 1:

            insights.append(
                f"{word.title()} appears frequently."
            )

        else:

            insights.append(
                f"{word.title()} has appeared in your history."
            )

    if len(insights) > 0:

        insights.append(
            "Monitor recurring symptoms carefully."
        )

    return insights