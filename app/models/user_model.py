from app.models.base_model import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "Users"
    
    Id = Column(String(255), primary_key=True)
    FullName = Column(Text, nullable=False)
    AvatarUrl = Column(Text, nullable=True)
    UserName = Column(String(256), nullable=True)
    NormalizedUserName = Column(String(256), nullable=True)
    Email = Column(String(256), nullable=True)
    NormalizedEmail = Column(String(256), nullable=True)
    EmailConfirmed = Column(Boolean, nullable=False, default=False)
    PasswordHash = Column(Text, nullable=True)
    SecurityStamp = Column(Text, nullable=True)
    ConcurrencyStamp = Column(Text, nullable=True)
    PhoneNumber = Column(Text, nullable=True)
    PhoneNumberConfirmed = Column(Boolean, nullable=False, default=False)
    TwoFactorEnabled = Column(Boolean, nullable=False, default=False)
    LockoutEnd = Column(DateTime(6), nullable=True)
    LockoutEnabled = Column(Boolean, nullable=False, default=True)
    AccessFailedCount = Column(Integer, nullable=False, default=0)

    # Relationships can be added here if needed, e.g.:
    # claims = relationship("UserClaim", back_populates="user")
    # roles = relationship("UserRole", back_populates="user")
    
class Role(Base):
    __tablename__ = "Roles"
    
    Id = Column(String(255), primary_key=True)
    Name = Column(String(256), nullable=True)
    NormalizedName = Column(String(256), nullable=True)
    ConcurrencyStamp = Column(Text, nullable=True)

class UserClaim(Base):
    __tablename__ = "UserClaims"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    UserId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), nullable=False)
    ClaimType = Column(Text, nullable=True)
    ClaimValue = Column(Text, nullable=True)

class UserRole(Base):
    __tablename__ = "UserRoles"
    
    UserId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), primary_key=True)
    RoleId = Column(String(255), ForeignKey("Roles.Id", ondelete='CASCADE'), primary_key=True)

class UserToken(Base):
    __tablename__ = "UserTokens"
    
    UserId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), primary_key=True)
    LoginProvider = Column(String(255), primary_key=True)
    Name = Column(String(255), primary_key=True)
    Value = Column(Text, nullable=True)

class UserLogin(Base):
    __tablename__ = "UserLogins"
    
    LoginProvider = Column(String(255), primary_key=True)
    ProviderKey = Column(String(255), primary_key=True)
    ProviderDisplayName = Column(Text, nullable=True)
    UserId = Column(String(255), ForeignKey("Users.Id", ondelete='CASCADE'), nullable=False)

class RoleClaim(Base):
    __tablename__ = "RoleClaims"
    
    Id = Column(Integer, primary_key=True, autoincrement=True)
    RoleId = Column(String(255), ForeignKey("Roles.Id", ondelete='CASCADE'), nullable=False)
    ClaimType = Column(Text, nullable=True)
    ClaimValue = Column(Text, nullable=True)
