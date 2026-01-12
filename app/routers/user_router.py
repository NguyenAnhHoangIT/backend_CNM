from fastapi import APIRouter
from app.schemas.user_schema import UserCreate, UserLogin, User as UserSchema, Token, UserMeResponse
from app.models.user_model import User, UserRole, Role
from app.db.base import get_db
from sqlalchemy.orm import Session, joinedload
from fastapi import Depends, HTTPException
from app.schemas.base_schema import DataResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.middleware.authenticate import authenticate
import uuid

router = APIRouter()


@router.post("/register", tags=["users"], description="Register a new user", response_model=DataResponse[UserSchema])
async def register_user(data: UserCreate, db: Session = Depends(get_db)):
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
             # Fallback or log error? User request implies we should find it. 
             # For now, let's assuming it exists as verified. 
             # But if not, we might fail constraint or just not assign role?
             # Better to raise error or print.
             print("Error: Customer role not found in DB")
             # Returning 500 might be appropriate if role is mandatory
             raise Exception("Customer role not found")
        
        db.commit()
        db.refresh(user)
        return DataResponse.custom_response(code="201", message="Register user success", data=user)
    except Exception as e:
        print(e)
        return DataResponse.custom_response(code="500", message="Register user failed", data=None)


@router.post("/login", tags=["users"], description="Login a user", response_model=DataResponse[Token])
async def login_user(data: UserLogin, db: Session = Depends(get_db)): 
    user = db.query(User).filter(User.Email == data.Email).first()
    if not user:
        return DataResponse.custom_response(code="401", message="Invalid email or password", data=None)
    if not verify_password(data.Password, user.PasswordHash):
        return DataResponse.custom_response(code="401", message="Invalid email or password", data=None)
    
    token = create_access_token(user.Id)
    
    return DataResponse.custom_response(code="200", message="Login user success", data=Token(access_token=token, token_type="Bearer"))

@router.get("/me", tags=["users"], description="Get current user", response_model=DataResponse[UserMeResponse], dependencies=[Depends(authenticate)])
async def get_current_user(current_user: User = Depends(authenticate)):
    return DataResponse.custom_response(code="200", message="Get current user success", data=current_user)

@router.get("/users", tags=["users"], description="Get all users", response_model=DataResponse[list[UserSchema]], dependencies=[Depends(authenticate)])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).options(joinedload(User.Roles)).all()
    return DataResponse.custom_response(code="200", message="Get all users success", data=users)
