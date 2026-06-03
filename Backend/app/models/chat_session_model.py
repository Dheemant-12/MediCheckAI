from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.database.connection import Base


class ChatSession(Base):

    __tablename__ = "chat_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    title = Column(
        String
    )