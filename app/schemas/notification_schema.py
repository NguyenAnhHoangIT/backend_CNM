from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    Title: str
    Content: str
    CreateAt: datetime
    ReadAt: Optional[datetime] = None
    Status: int
    ReceiverId: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    Id: int
    class Config:
        from_attributes = True
