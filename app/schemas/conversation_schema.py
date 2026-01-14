from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.user_schema import UserMeResponse
from app.schemas.message_schema import Message

class ConversationBase(BaseModel):
    CustomerId: str
    AdminId: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    Id: int
    CreatedAt: datetime
    LastMessageAt: Optional[datetime] = None
    Customer: Optional[UserMeResponse] = None
    Admin: Optional[UserMeResponse] = None
    Messages: List[Message] = []

    class Config:
        from_attributes = True
