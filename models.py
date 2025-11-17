from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class CallSignal(Base):
    tablename = "call_signals"

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(Integer, index=True)
    to_id = Column(Integer, index=True)
    type = Column(String, index=True)  # offer / answer / candidate
    content = Column(String)           # JSON-строка SDP або candidate
    created_at = Column(DateTime, default=datetime.utcnow)
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    telegram_id = Column(Integer, nullable=True)
    token = Column(String, unique=True, index=True, nullable=False)
    pubkey = Column(String, nullable=True)

    messages_from = relationship("Message", back_populates="from_user", foreign_keys="Message.from_id")
    messages_to = relationship("Message", back_populates="to_user", foreign_keys="Message.to_id")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    from_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    to_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    iv = Column(String, nullable=False)
    ciphertext = Column(String, nullable=False)
    msg_type = Column(String, nullable=False, default="text")
    ttl_sec = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    from_user = relationship("User", foreign_keys=[from_id], back_populates="messages_from")
    to_user = relationship("User", foreign_keys=[to_id], back_populates="messages_to")
