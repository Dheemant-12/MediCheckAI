from fastapi import APIRouter, Depends

from app.database.connection import SessionLocal

from app.models.chat_session_model import (
    ChatSession
)

from app.security.current_user import (
    get_current_user
)

router = APIRouter()


@router.post("/session")
def create_session(
    data: dict,
    current_user = Depends(
        get_current_user
    )
):

    title = data.get(
        "title",
        "New Conversation"
    )

    db = SessionLocal()

    session = ChatSession(
        user_id=current_user.id,
        title=title
    )

    db.add(session)

    db.commit()

    db.refresh(session)

    db.close()

    return {
        "session_id": session.id,
        "title": session.title
    }


@router.get("/sessions")
def get_sessions(
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    sessions = db.query(
        ChatSession
    ).filter(
        ChatSession.user_id ==
        current_user.id
    ).all()

    result = []

    for session in sessions:

        result.append({
            "id": session.id,
            "title": session.title
        })

    db.close()

    return result
@router.put("/session/{session_id}")
def update_session_title(
    session_id: int,
    data: dict,
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    session = db.query(
        ChatSession
    ).filter(
        ChatSession.id == session_id,
        ChatSession.user_id ==
        current_user.id
    ).first()

    if not session:

        db.close()

        return {
            "message":
            "Session not found"
        }

    session.title = data.get(
        "title",
        session.title
    )

    db.commit()

    db.refresh(session)

    db.close()

    return {
        "message":
        "Title updated",
        "title":
        session.title
    }
@router.delete("/session/{session_id}")
def delete_session(
    session_id: int,
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    session = db.query(
        ChatSession
    ).filter(
        ChatSession.id == session_id,
        ChatSession.user_id ==
        current_user.id
    ).first()

    if not session:

        db.close()

        return {
            "message":
            "Session not found"
        }

    from app.models.chat_model import (
        ChatHistory
    )

    db.query(
        ChatHistory
    ).filter(
        ChatHistory.session_id ==
        session_id
    ).delete()

    db.delete(session)

    db.commit()

    db.close()

    return {
        "message":
        "Session deleted"
    }