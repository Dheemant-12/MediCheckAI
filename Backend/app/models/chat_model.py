from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey
)

from app.database.connection import Base


class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    user_message = Column(
        Text
    )

    ai_response = Column(
        Text
    )