from fastapi import APIRouter, Depends

from fastapi.responses import FileResponse

from reportlab.pdfgen import canvas

from app.database.connection import SessionLocal

from app.models.chat_model import ChatHistory
from app.models.chat_session_model import ChatSession

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

    session = db.query(
        ChatSession
    ).filter(
        ChatSession.id ==
        session_id
    ).first()

    file_name = (
        f"session_{session_id}.pdf"
    )

    pdf = canvas.Canvas(
        file_name
    )

    y = 800

    pdf.setFont(
    "Helvetica-Bold",
    18
)

    pdf.drawString(
            50,
            y,
            "MediCheck AI Health Report"
        )

    y -= 40

    pdf.setFont(
       "Helvetica",
        12
    )

    pdf.drawString(
        50,
        y,
        f"Patient: {current_user.username}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Email: {current_user.email}"
    )

    y -= 20

    pdf.drawString(
        50,
        y,
        f"Conversation: {session.title}"
    )

    y -= 40
    pdf.setFont(
    "Helvetica-Bold",
    14
)

    pdf.drawString(
        50,
        y,
        "Conversation History"
    )

    y -= 30

    pdf.setFont(
        "Helvetica",
        11
    )


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
            "AI Response:"
        )

        y -= 20

        pdf.drawString(
            70,
            y,
            chat.ai_response[:150]
        )

        y -= 40

        if y < 100:

            pdf.showPage()

            y = 800

    y -= 20

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Summary"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    pdf.drawString(
        50,
        y,
        f"Total Messages: {len(chats)}"
    )

    pdf.save()

    db.close()

    return FileResponse(
        file_name,
        media_type=
        "application/pdf",
        filename=file_name
    )    