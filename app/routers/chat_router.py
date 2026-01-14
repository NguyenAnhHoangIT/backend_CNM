from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from typing import List, Dict
from sqlalchemy.orm import Session, joinedload
from app.db.base import get_db
from app.middleware.authenticate import authenticate
from app.models.conversation_model import Conversation
from app.models.message_model import Message
from app.models.user_model import User
from app.schemas.conversation_schema import Conversation as ConversationSchema, ConversationCreate
from app.schemas.message_schema import Message as MessageSchema, MessageCreate
from app.schemas.base_schema import DataResponse
from datetime import datetime
import json

router = APIRouter()

# Connection Manager for WebSockets
class ConnectionManager:
    def __init__(self):
        # Map user_id to a list of active websockets (user might be logged in on multiple devices)
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception as e:
                    print(f"Error sending message to {user_id}: {e}")

manager = ConnectionManager()

@router.websocket("/ws/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Keep connection alive, maybe handle incoming messages if we wanted full bidirectional WS
            # For now, we only use it for pushing notifications
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

@router.get("/conversations", tags=["chat"], description="Get all conversations for current user", response_model=DataResponse[list[ConversationSchema]])
def get_conversations(db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    user_id = user.Id
    
    # Fetch conversations where the user is either the Customer or the Admin
    conversations = db.query(Conversation).options(
        joinedload(Conversation.Customer),
        joinedload(Conversation.Admin)
    ).filter(
        (Conversation.CustomerId == user_id) | (Conversation.AdminId == user_id)
    ).order_by(Conversation.LastMessageAt.desc()).all()
    
    return DataResponse.custom_response(code="200", message="Get conversations success", data=conversations)

@router.post("/conversations", tags=["chat"], description="Create or get existing conversation", response_model=DataResponse[ConversationSchema])
def create_conversation(data: ConversationCreate, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    # Check if conversation already exists
    existing_conversation = db.query(Conversation).filter(
        Conversation.CustomerId == data.CustomerId,
        Conversation.AdminId == data.AdminId
    ).options(
        joinedload(Conversation.Customer),
        joinedload(Conversation.Admin)
    ).first()

    if existing_conversation:
        return DataResponse.custom_response(code="200", message="Conversation found", data=existing_conversation)

    new_conversation = Conversation(
        CustomerId=data.CustomerId,
        AdminId=data.AdminId,
        CreatedAt=datetime.now(),
        LastMessageAt=datetime.now()
    )

    try:
        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)
        # Re-fetch with relationships
        new_conversation = db.query(Conversation).options(
            joinedload(Conversation.Customer),
            joinedload(Conversation.Admin)
        ).filter(Conversation.Id == new_conversation.Id).first()
        
        return DataResponse.custom_response(code="201", message="Create conversation success", data=new_conversation)
    except Exception as e:
        print(f"Error creating conversation: {e}")
        return DataResponse.custom_response(code="500", message="Create conversation failed", data=None)

@router.get("/conversations/{conversation_id}/messages", tags=["chat"], description="Get messages for a conversation", response_model=DataResponse[list[MessageSchema]])
def get_messages(conversation_id: int, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    # Access control: user must be part of the conversation
    conversation = db.query(Conversation).filter(Conversation.Id == conversation_id).first()
    if not conversation:
        return DataResponse.custom_response(code="404", message="Conversation not found", data=None)
    
    if conversation.CustomerId != user.Id and conversation.AdminId != user.Id:
        return DataResponse.custom_response(code="403", message="Not authorized to view this conversation", data=None)

    messages = db.query(Message).options(joinedload(Message.Sender)).filter(
        Message.ConversationId == conversation_id
    ).order_by(Message.CreatedAt.asc()).all()

    return DataResponse.custom_response(code="200", message="Get messages success", data=messages)

@router.post("/conversations/{conversation_id}/messages", tags=["chat"], description="Send a message", response_model=DataResponse[MessageSchema])
async def send_message(conversation_id: int, data: MessageCreate, db: Session = Depends(get_db), user: dict = Depends(authenticate)):
    # Verify conversation exists and user is participant
    conversation = db.query(Conversation).filter(Conversation.Id == conversation_id).first()
    if not conversation:
        return DataResponse.custom_response(code="404", message="Conversation not found", data=None)
    
    if conversation.CustomerId != user.Id and conversation.AdminId != user.Id:
        return DataResponse.custom_response(code="403", message="Not authorized to send message to this conversation", data=None)

    new_message = Message(
        ConversationId=conversation_id,
        SenderId=user.Id,
        Content=data.Content,
        MessageType=data.MessageType,
        IsRead=False,
        CreatedAt=datetime.now()
    )

    try:
        db.add(new_message)
        # Update LastMessageAt
        conversation.LastMessageAt = datetime.now()
        db.commit()
        db.refresh(new_message)
        # Re-fetch with sender
        new_message = db.query(Message).options(joinedload(Message.Sender)).filter(Message.Id == new_message.Id).first()
        
        # Prepare message for broadcast
        # Manually construct dict or use schema serialization if possible, but schema objects aren't JSON serializable by default without pydantic's help
        # Let's simple dict for now
        msg_data = {
            "Id": new_message.Id,
            "ConversationId": new_message.ConversationId,
            "SenderId": new_message.SenderId,
            "Content": new_message.Content,
            "MessageType": new_message.MessageType,
            "CreatedAt": new_message.CreatedAt.isoformat(),
            "Sender": {
                "FullName": new_message.Sender.FullName if new_message.Sender else "Unknown",
                "AvatarUrl": new_message.Sender.AvatarUrl if new_message.Sender else None
            }
        }
        
        # Determine Recipient (The other person in the conversation)
        recipient_id = conversation.AdminId if conversation.CustomerId == user.Id else conversation.CustomerId
        
        # Send to Recipient
        await manager.send_personal_message(msg_data, recipient_id)
        # Send to Sender (confirmation) - optional, but good for real-time UI consistency if not using optimistic UI
        # await manager.send_personal_message(msg_data, user.Id)
        
        return DataResponse.custom_response(code="201", message="Send message success", data=new_message)
    except Exception as e:
        print(f"Error sending message: {e}")
        return DataResponse.custom_response(code="500", message="Send message failed", data=None)
