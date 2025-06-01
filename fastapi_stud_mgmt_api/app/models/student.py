from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    grade: int = Field(..., ge=1, le=12, description="Grade must be between 1 and 12")
    age: int = Field(..., gt=0, lt=18, description="Age must be less than 18")
    address: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    grade: Optional[int] = Field(None, ge=1, le=12, description="Grade must be between 1 and 12")
    age: Optional[int] = Field(None, gt=0, lt=18, description="Age must be less than 18")
    address: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)


class StudentResponse(StudentBase):
    id: str

    class Config:
        from_attributes = True