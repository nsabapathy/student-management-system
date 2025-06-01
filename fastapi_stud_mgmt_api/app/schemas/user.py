from pydantic import BaseModel, EmailStr
from typing import Optional


class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True