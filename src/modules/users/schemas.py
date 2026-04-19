from typing import Literal, Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

from src.modules.users.models import UserRole


class BaseUserSchema(BaseModel):
    """Base user schema"""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.lower()

class UserCreateSchema(BaseUserSchema):
    """User register schema"""
    username: str = Field(..., min_length=2, max_length=50)

class UserUpdateSchema(BaseModel):
    """User update schema"""
    username: Optional[str] = Field(None, min_length=2, max_length=50)

class UserReadSchema(BaseModel):
    """Read user schema"""
    id: int
    username: str
    email: str

    role: UserRole
    
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str

class AdminUpdateUserSchema(BaseModel):
    username: str | None = Field(None, min_length=2, max_length=50)
    role: UserRole | None = None
    is_active: bool | None = None

class RequestUserMeta(BaseModel): 
    page: int = Field(..., ge=1)        # Текущая страница
    size: int = Field(..., ge=1)        # Кол-во на странице
 
    sort_by: Literal["username", "created_at"] = "created_at"
    order: Literal["asc", "desc"] = "desc"

    role: UserRole | None = None
    is_active: bool | None = None
