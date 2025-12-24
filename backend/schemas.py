# backend/schemas.py

from pydantic import BaseModel
from typing import Optional

# نموذج مستخدم للطلبات والاستجابات
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    language: Optional[str] = "en"

# عند تسجيل مستخدم جديد
class UserCreate(UserBase):
    password: str

# عند إرسال بيانات المستخدم كرد على API
class UserResponse(UserBase):
    class Config:
        orm_mode = True

# نموذج لتسجيل الدخول
class UserLogin(BaseModel):
    username: str
    password: str
