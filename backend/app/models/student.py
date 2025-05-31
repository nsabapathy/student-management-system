from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        json_schema = handler(core_schema)
        json_schema.update(type="string")
        return json_schema

class StudentBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    grade_level: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    age: int = Field(..., ge=5, le=17)
    address: str = Field(..., min_length=10, max_length=200)
    role: str = Field(..., pattern='^(student|teacher)$')

class StudentCreate(StudentBase):
    pass

class StudentInDB(StudentBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    grade_level: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = Field(None, max_length=500)
    age: Optional[int] = Field(None, ge=5, le=17)
    address: Optional[str] = Field(None, min_length=10, max_length=200)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Student(StudentInDB):
    pass
