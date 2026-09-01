from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    description: Optional[str]

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_id: int

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    role: Role

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
