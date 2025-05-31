from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.student import Student, StudentCreate, StudentUpdate
from app.database.connection import Database
from bson import ObjectId

router = APIRouter(prefix="/students", tags=["students"])
db = Database.get_db()

@router.get("/", response_model=List[Student])
async def get_all_students():
    students = await db["students"].find().to_list(1000)
    return [Student(**student, id=str(student["_id"])) for student in students]

@router.post("/", response_model=Student)
async def create_student(student: StudentCreate):
    new_student = student.dict()
    result = await db["students"].insert_one(new_student)
    created_student = await db["students"].find_one({"_id": result.inserted_id})
    return Student(**created_student, id=str(created_student["_id"]))

@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = await db["students"].find_one({"_id": ObjectId(student_id)})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return Student(**student, id=str(student["_id"]))

@router.put("/{student_id}", response_model=Student)
async def update_student(student_id: str, student_update: StudentUpdate):
    updated_student = await db["students"].find_one_and_update(
        {"_id": ObjectId(student_id)},
        {"$set": student_update.dict(exclude_unset=True)},
        return_document=True
    )
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return Student(**updated_student, id=str(updated_student["_id"]))

@router.delete("/{student_id}")
async def delete_student(student_id: str):
    delete_result = await db["students"].delete_one({"_id": ObjectId(student_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
