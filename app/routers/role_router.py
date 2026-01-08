from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.middleware.authenticate import authenticate
from app.models.user_model import Role, UserRole, User
from app.schemas.user_schema import Role as RoleSchema, RoleBase
from app.schemas.base_schema import DataResponse
import uuid

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    dependencies=[Depends(authenticate)] 
)

@router.get("", description="List all roles", response_model=DataResponse[list[RoleSchema]])
async def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return DataResponse.custom_response(code="200", message="Get roles success", data=roles)

@router.post("", description="Create a new role", response_model=DataResponse[RoleSchema])
async def create_role(role_in: RoleBase, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.Name == role_in.Name).first()
    if role:
        return DataResponse.custom_response(code="400", message="Role already exists", data=None)
    
    new_role = Role(
        Id=str(uuid.uuid4()),
        Name=role_in.Name,
        NormalizedName=role_in.Name.upper()
    )
    db.add(new_role)
    try:
        db.commit()
        db.refresh(new_role)
        return DataResponse.custom_response(code="201", message="Create role success", data=new_role)
    except Exception as e:
        print(f"Error creating role: {e}")
        return DataResponse.custom_response(code="500", message="Create role failed", data=None)

@router.post("/users/{user_id}", description="Assign role to user")
async def assign_role_to_user(user_id: str, role_id: str = None, role_name: str = None, db: Session = Depends(get_db)):
    # Verify user exists
    user = db.query(User).filter(User.Id == user_id).first()
    if not user:
        return DataResponse.custom_response(code="404", message="User not found", data=None)
    
    role = None
    if role_id:
        role = db.query(Role).filter(Role.Id == role_id).first()
    elif role_name:
        role = db.query(Role).filter(Role.Name == role_name).first()
        
    if not role:
        return DataResponse.custom_response(code="404", message="Role not found", data=None)
        
    # Check if assignment exists
    user_role = db.query(UserRole).filter(UserRole.UserId == user_id, UserRole.RoleId == role.Id).first()
    if user_role:
        return DataResponse.custom_response(code="400", message="User already has this role", data=None)
        
    new_user_role = UserRole(UserId=user_id, RoleId=role.Id)
    db.add(new_user_role)
    try:
        db.commit()
        return DataResponse.custom_response(code="200", message="Role assigned to user success", data=None)
    except Exception as e:
        print(f"Error assigning role: {e}")
        return DataResponse.custom_response(code="500", message="Assign role failed", data=None)
