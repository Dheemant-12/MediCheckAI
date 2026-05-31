from sqlalchemy import Column, Integer, Text

from app.database.connection import Base

class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_message = Column(
        Text
    )

    ai_response = Column(
        Text
    )