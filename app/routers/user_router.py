from fastapi import APIRouter, File, UploadFile, Form
from app.schemas.user_schema import UserCreate, UserLogin, User as UserSchema, Token, UserMeResponse, UserLoginResponse, UserAdminCreate, UserAdminUpdate
from app.models.user_model import User, UserRole, Role
from app.db.base import get_db
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException
from app.schemas.base_schema import DataResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.middleware.authenticate import authenticate
import uuid
from typing import Optional
import cloudinary.uploader
from app.core.config import settings

from app.core.config import settings
from fastapi import BackgroundTasks
from app.utils.email import send_welcome_email

from app.models.conversation_model import Conversation
from app.models.message_model import Message
from datetime import datetime

router = APIRouter()


@router.post("/register", tags=["users"], description="Register a new user", response_model=DataResponse[UserSchema])
async def register_user(data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.Email == data.Email).first()
    if existing:
        return DataResponse.custom_response(code="400", message="Email already exists", data=None)

    password_hash = hash_password(data.Password)
    user_id = str(uuid.uuid4())
    
    user = User(
        Id=user_id,
        FullName=data.FullName,
        Email=data.Email,
        UserName=data.UserName,
        PasswordHash=password_hash,
        EmailConfirmed=False,
        # Default others
    )
    
    try:
        db.add(user)
        db.flush() # Flush to ensure user exists before adding role if needed (though Id is pre-generated)
        
        # Assign default Customer role
        customer_role = db.query(Role).filter(Role.Name == "Customer").first()
        if customer_role:
             user_role = UserRole(UserId=user.Id, RoleId=customer_role.Id)
             db.add(user_role)
        else:
             print("Error: Customer role not found in DB")
             raise Exception("Customer role not found")
        
        # --- Automatic Conversation Creation with Admin ---
        ADMIN_ID = "db0e6986-0d48-4b16-8d00-d5a95ba77f95"
        
        # Check if Admin exists (Optional but safer)
        admin_user = db.query(User).filter(User.Id == ADMIN_ID).first()
        if admin_user:
            # Create Conversation
            new_conversation = Conversation(
                CustomerId=user.Id,
                AdminId=ADMIN_ID,
                CreatedAt=datetime.now(),
                LastMessageAt=datetime.now()
            )
            db.add(new_conversation)
            db.flush() # Flush to get Conversation ID

            # Create Welcome Message
            welcome_message = Message(
                ConversationId=new_conversation.Id,
                SenderId=ADMIN_ID,
                Content="Chào mừng bạn đến với shop",
                MessageType="text", # Assuming 'text' is the standard type based on common practices, or empty string if enum not strict? 
                # Checking chat_router.py showed usage of data.MessageType. usually it's "text" or "image".
                IsRead=False,
                CreatedAt=datetime.now()
            )
            db.add(welcome_message)
        else:
            print(f"Warning: Admin with ID {ADMIN_ID} not found. Welcome conversation not created.")

        db.commit()
        db.refresh(user)
        
        # Send welcome email
        background_tasks.add_task(send_welcome_email, user.Email, user.FullName) 
        
        return DataResponse.custom_response(code="201", message="Register user success", data=user)
    except Exception as e:
        print(e)
        return DataResponse.custom_response(code="500", message="Register user failed", data=None)


@router.post("/login", tags=["users"], description="Login a user", response_model=DataResponse[UserLoginResponse])
async def login_user(data: UserLogin, db: Session = Depends(get_db)): 
    # Eager load Roles for response
    user = db.query(User).options(joinedload(User.Roles)).filter(User.Email == data.Email).first()
    if not user:
        return DataResponse.custom_response(code="401", message="Invalid email or password", data=None)
    if not verify_password(data.Password, user.PasswordHash):
        return DataResponse.custom_response(code="401", message="Invalid email or password", data=None)
    
    token = create_access_token(user.Id)
    
    # Get primary role name
    role_name = user.Roles[0].Name if user.Roles else None
    
    return DataResponse.custom_response(
        code="200", 
        message="Login user success", 
        data=UserLoginResponse(
            access_token=token, 
            token_type="Bearer",
            UserName=user.UserName,
            FullName=user.FullName,
            Email=user.Email,
            Role=role_name,
            AvatarUrl=user.AvatarUrl
        )
    )

@router.get("/me", tags=["users"], description="Get current user", response_model=DataResponse[UserMeResponse], dependencies=[Depends(authenticate)])
async def get_current_user(current_user: User = Depends(authenticate)):
    return DataResponse.custom_response(code="200", message="Get current user success", data=current_user)

@router.put("/me", tags=["users"], description="Update current user profile", response_model=DataResponse[UserMeResponse], dependencies=[Depends(authenticate)])
async def update_current_user(
    FullName: Optional[str] = Form(None),
    UserName: Optional[str] = Form(None),
    PhoneNumber: Optional[str] = Form(None),
    OldPassword: Optional[str] = Form(None),
    NewPassword: Optional[str] = Form(None),
    Avatar: Optional[UploadFile] = File(None),
    current_user: User = Depends(authenticate),
    db: Session = Depends(get_db)
):
    # 1. Check UserName uniqueness if changed
    if UserName and UserName != current_user.UserName:
        existing_username = db.query(User).filter(User.UserName == UserName).first()
        if existing_username:
            return DataResponse.custom_response(code="400", message="Username already exists", data=None)
        current_user.UserName = UserName

    # 2. Update simple fields
    if FullName:
        current_user.FullName = FullName
    if PhoneNumber:
        current_user.PhoneNumber = PhoneNumber

    # 3. Update Password
    if NewPassword:
        if not OldPassword:
            return DataResponse.custom_response(code="400", message="Old password is required to set a new password", data=None)
        if not verify_password(OldPassword, current_user.PasswordHash):
             return DataResponse.custom_response(code="400", message="Incorrect old password", data=None)
        current_user.PasswordHash = hash_password(NewPassword)

    # 4. Update Avatar
    if Avatar:
        try:
            # Calculate folder path or name if needed, using default for now
            # Note: Cloudinary config should be loaded globally
            result = cloudinary.uploader.upload(Avatar.file, folder="user_avatars")
            current_user.AvatarUrl = result.get("secure_url")
        except Exception as e:
            print(f"Cloudinary upload failed: {e}")
            return DataResponse.custom_response(code="500", message="Failed to upload avatar", data=None)

    try:
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return DataResponse.custom_response(code="200", message="Update profile success", data=current_user)
    except Exception as e:
        print(e)
        db.rollback()
        return DataResponse.custom_response(code="500", message="Update profile failed", data=None)

@router.get("/users", tags=["users"], description="Get all users", response_model=DataResponse[list[UserSchema]], dependencies=[Depends(authenticate)])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).options(joinedload(User.Roles)).all()
    return DataResponse.custom_response(code="200", message="Get all users success", data=users)

@router.post("/users", tags=["users"], description="Admin create user", response_model=DataResponse[UserSchema], dependencies=[Depends(authenticate)])
async def admin_create_user(data: UserAdminCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.Email == data.Email).first()
    if existing:
        return DataResponse.custom_response(code="400", message="Email already exists", data=None)

    password_hash = hash_password(data.Password)
    user_id = str(uuid.uuid4())
    
    user = User(
        Id=user_id,
        FullName=data.FullName,
        Email=data.Email,
        UserName=data.UserName,
        PasswordHash=password_hash,
        Status=data.Status, # Admin can set status
        PhoneNumber=data.PhoneNumber,
        EmailConfirmed=True, # Admin created usually active/verified
        PhoneNumberConfirmed=True,
    )
    
    try:
        db.add(user)
        db.flush()
        
        # Assign role
        role_id = data.RoleId
        if not role_id:
             # Default to Customer if not provided
             customer_role = db.query(Role).filter(Role.Name == "Customer").first()
             if customer_role:
                 role_id = customer_role.Id
        
        if role_id:
             user_role = UserRole(UserId=user.Id, RoleId=role_id)
             db.add(user_role)
        
        db.commit()
        db.refresh(user)
        # Re-query with roles
        user = db.query(User).options(joinedload(User.Roles)).filter(User.Id == user.Id).first()
        
        # Send welcome email
        background_tasks.add_task(send_welcome_email, user.Email, user.FullName)
        
        return DataResponse.custom_response(code="201", message="Create user success", data=user)
    except Exception as e:
        print(e)
        return DataResponse.custom_response(code="500", message="Create user failed", data=None)

@router.get("/users/{id}", tags=["users"], description="Get user by id", response_model=DataResponse[UserSchema], dependencies=[Depends(authenticate)])
async def get_user_by_id(id: str, db: Session = Depends(get_db)):
    user = db.query(User).options(joinedload(User.Roles)).filter(User.Id == id).first()
    if not user:
        return DataResponse.custom_response(code="404", message="User not found", data=None)
    return DataResponse.custom_response(code="200", message="Get user success", data=user)

@router.put("/users/{id}", tags=["users"], description="Update user by id", response_model=DataResponse[UserSchema], dependencies=[Depends(authenticate)])
async def update_user(id: str, data: UserAdminUpdate, db: Session = Depends(get_db)):
    user = db.query(User).options(joinedload(User.Roles)).filter(User.Id == id).first()
    if not user:
        return DataResponse.custom_response(code="404", message="User not found", data=None)
    
    if data.FullName is not None:
        user.FullName = data.FullName
    if data.UserName is not None:
        # Check uniqueness if changed
        if user.UserName != data.UserName:
             existing = db.query(User).filter(User.UserName == data.UserName).first()
             if existing:
                 return DataResponse.custom_response(code="400", message="Username already exists", data=None)
        user.UserName = data.UserName
    if data.Email is not None:
        if user.Email != data.Email:
             existing = db.query(User).filter(User.Email == data.Email).first()
             if existing:
                 return DataResponse.custom_response(code="400", message="Email already exists", data=None)
        user.Email = data.Email
    if data.PhoneNumber is not None:
        user.PhoneNumber = data.PhoneNumber
    if data.Status is not None:
        user.Status = data.Status
    if data.AvatarUrl is not None:
        user.AvatarUrl = data.AvatarUrl
    
    if data.Password:
        user.PasswordHash = hash_password(data.Password)
        
    try:
        # Handle Role update if RoleId is provided
        if data.RoleId:
            # Remove existing roles? Or replace? Usually replace primary for simple users
            # Assuming single role for now based on previous code logic (Roles[0])
            db.query(UserRole).filter(UserRole.UserId == user.Id).delete()
            new_role = UserRole(UserId=user.Id, RoleId=data.RoleId)
            db.add(new_role)
            
        db.commit()
        db.refresh(user)
        # Re-query
        user = db.query(User).options(joinedload(User.Roles)).filter(User.Id == user.Id).first()
        return DataResponse.custom_response(code="200", message="Update user success", data=user)
    except Exception as e:
        print(e)
        db.rollback()
        return DataResponse.custom_response(code="500", message="Update user failed", data=None)

@router.delete("/users/{id}", tags=["users"], description="Delete user", response_model=DataResponse[UserSchema], dependencies=[Depends(authenticate)])
async def delete_user(id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.Id == id).first()
    if not user:
        return DataResponse.custom_response(code="404", message="User not found", data=None)
    
    try:
        # Soft delete
        user.Status = 0
        db.commit()
        db.refresh(user)
        return DataResponse.custom_response(code="200", message="Delete user success", data=user)
    except Exception as e:
        print(e)
        db.rollback()
        return DataResponse.custom_response(code="500", message="Delete user failed", data=None)
