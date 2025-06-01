from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentInDB(BaseModel):
    name: str
    email: EmailStr
    grade: int
    age: int
    address: str
    description: Optional[str] = None