from typing import List
from pydantic import BaseModel, ConfigDict,EmailStr
from datetime import datetime
from pydantic import  constr, field_validator, ValidationError
import re

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "admin",
                    "password": "admin",
                    "role_id": 1
                }
            ]
        }
    }


class UserPublicInfo(BaseModel):
    id: int
    username: str
    role_id: int
    activated: bool
    created_at: datetime
    updated_at: datetime | None = None
    first_name: str
    last_name: str
    email: EmailStr

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "admin",
                    "role_id": 1,
                    "activated": 1,
                    "created_at": "2020-10-15T20:40:10",
                    "updated_at": "2020-10-15T20:45:08",
                    "first_name": "Admin",
                    "last_name": "User",
                    "email": "admin@example.com"
                }
            ]
        }
    }


class User(UserPublicInfo):
    model_config = ConfigDict(from_attributes=True)


class UserCreated(UserPublicInfo):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "username": "admin",
                    "password": "password",
                    "role_id": 1,
                    "activated": 1,
                    "created_at": "2020-10-15T20:40:10",
                    "updated_at": "2020-10-15T20:45:08"
                }
            ]
        }
    }


class UserUpdate(BaseModel):
    username: str | None = None
    password: str | None = None
    role_id: int | None = None
    activated: bool | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "admin",
                    "password": "admin",
                    "role_id": 1,
                    "activated": 1
                }
            ]
        }
    }


class UserHashedPassword(UserPublicInfo):
    hashed_password: str


class UserPublicInfoList(BaseModel):
    page: int
    limit: int
    total: int
    users: List[User]

class UserRegister(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8, max_length=128)
    first_name: constr(min_length=3, max_length=50)
    last_name: constr(min_length=3, max_length=50)
    email: EmailStr 
    phone: constr(min_length=3, max_length=15)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        # At least one uppercase, one lowercase, one digit, one special character
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v