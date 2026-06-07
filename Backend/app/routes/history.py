from fastapi import APIRouter, Depends

from fastapi.responses import FileResponse

from reportlab.pdfgen import canvas

from app.database.connection import SessionLocal

from app.models.chat_model import ChatHistory

from app.security.current_user import (
    get_current_user
)


router = APIRouter()


@router.get("/history")
def get_history(
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    chats = db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user.id
    ).all()

    result = []

    for chat in chats:

        result.append({
            "user_message":
                chat.user_message,
            "ai_response":
                chat.ai_response
        })

    db.close()

    return result


@router.get("/session/{session_id}/history")
def get_session_history(
    session_id: int,
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    chats = db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user.id,
        ChatHistory.session_id ==
        session_id
    ).all()

    result = []

    for chat in chats:

        result.append({
            "user_message":
                chat.user_message,
            "ai_response":
                chat.ai_response
        })

    db.close()

    return result


@router.delete("/history")
def clear_history(
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user.id
    ).delete()

    db.commit()

    db.close()

    return {
        "message":
        "History cleared successfully"
    }
@router.get("/session/{session_id}/pdf")
def export_session_pdf(
    session_id: int,
    current_user = Depends(
        get_current_user
    )
):

    db = SessionLocal()

    chats = db.query(
        ChatHistory
    ).filter(
        ChatHistory.user_id ==
        current_user.id,
        ChatHistory.session_id ==
        session_id
    ).all()

    file_name = (
        f"session_{session_id}.pdf"
    )

    pdf = canvas.Canvas(
        file_name
    )

    y = 800

    pdf.drawString(
        50,
        y,
        f"MediCheck AI Report"
    )

    y -= 40

    for chat in chats:

        pdf.drawString(
            50,
            y,
            f"User: {chat.user_message}"
        )

        y -= 20

        pdf.drawString(
            50,
            y,
            f"AI: {chat.ai_response[:100]}"
        )

        y -= 40

        if y < 100:

            pdf.showPage()

            y = 800

    pdf.save()

    db.close()

    return FileResponse(
        file_name,
        media_type=
        "application/pdf",
        filename=file_name
    )    