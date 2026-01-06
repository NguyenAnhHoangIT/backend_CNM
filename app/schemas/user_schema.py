from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    FullName: str
    UserName: Optional[str] = None
    Email: Optional[str] = None # EmailStr? keeping simple for now
    PhoneNumber: Optional[str] = None
    AvatarUrl: Optional[str] = None
    TwoFactorEnabled: bool = False
    LockoutEnabled: bool = True

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
    LockoutEnd: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

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

class TokenData(BaseModel):
    username: Optional[str] = None

class TokenPayload(BaseModel):
    user_id: str
    exp: int
