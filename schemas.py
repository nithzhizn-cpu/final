from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    username: str
    telegram_id: Optional[int] = None


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class PubKeyUpdate(BaseModel):
    pubkey: str


class PubKeyOut(BaseModel):
    pubkey: str


class MessageCreate(BaseModel):
    to: int
    iv: str
    ciphertext: str
    msg_type: str = "text"
    ttl_sec: Optional[int] = None


class MessageOut(BaseModel):
    id: int
    from_id: int
    to_id: int
    iv: str
    ciphertext: str
    msg_type: str
    ttl_sec: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessagesResponse(BaseModel):
    messages: list[MessageOut]
