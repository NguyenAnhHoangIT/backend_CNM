from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    FullName: str
    UserName: Optional[str] = None
    Email: Optional[str] = None # EmailStr? keeping simple for now

class UserCreate(UserBase):
    Password: str
    ConfirmPassword: str

class UserUpdate(UserBase):
    Password: Optional[str] = None

class UserLogin(BaseModel):
    Email: str
    Password: str

class UserInDBBase(UserBase):
    Id: str 
    EmailConfirmed: bool = False
    PhoneNumberConfirmed: bool = False
    AccessFailedCount: int = 0
    AccessFailedCount: int = 0
    LockoutEnd: Optional[datetime] = None
    Status: int = 1
    
    class Config:
        from_attributes = True

class User(UserInDBBase):
    Roles: List["Role"] = []

class UserMeResponse(BaseModel):
    FullName: str
    UserName: Optional[str] = None
    Email: Optional[str] = None
    PhoneNumber: Optional[str] = None
    AvatarUrl: Optional[str] = None
    
    class Config:
        from_attributes = True

class RoleBase(BaseModel):
    Name: str

class Role(RoleBase):
    Id: str
    NormalizedName: Optional[str] = None
    
    class Config:
        from_attributes = True

# JWT Token schemas - Keep these standard snake_case as they follow OAuth spec/library defaults usually
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLoginResponse(Token):
    UserName: Optional[str] = None
    FullName: str
    Email: Optional[str] = None
    Role: Optional[str] = None
    AvatarUrl: Optional[str] = None

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenPayload(BaseModel):
    user_id: str
    exp: int
