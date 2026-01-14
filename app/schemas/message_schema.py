from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.schemas.user_schema import UserMeResponse

class MessageBase(BaseModel):
    Content: str
    MessageType: Optional[str] = 'text'

class MessageCreate(MessageBase):
    ConversationId: int

class Message(MessageBase):
    Id: int
    ConversationId: int
    SenderId: str
    IsRead: bool
    CreatedAt: datetime
    Sender: Optional[UserMeResponse] = None

    class Config:
        from_attributes = True
