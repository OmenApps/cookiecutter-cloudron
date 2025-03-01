from datetime import datetime
from typing import List, Optional

from ninja import Schema
from pydantic import EmailStr, field_validator


class TokenSchema(Schema):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserBasicSchema(Schema):
    id: int
    email: EmailStr
    name: str
    is_active: bool
    date_joined: datetime

class UserDetailSchema(UserBasicSchema):
    last_login: Optional[datetime]
    is_staff: bool
    is_superuser: bool
    groups: List[str]
    mfa_enabled: bool
    {% if cookiecutter.use_cloudron_auth == "yes" %}cloudron_user_id: Optional[str]{% endif %}


class UserCreateSchema(Schema):
    email: EmailStr
    password: str
    name: str

    @field_validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserUpdateSchema(Schema):
    name: Optional[str]
    email: Optional[EmailStr]
    is_active: Optional[bool]

class PasswordChangeSchema(Schema):
    current_password: str
    new_password: str

    @field_validator('new_password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class LoginSchema(Schema):
    email: EmailStr
    password: str
    mfa_code: Optional[str]
