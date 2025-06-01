from typing import List, Optional
from bson import ObjectId
from app.database import get_database
from app.models.student import StudentCreate, StudentUpdate, StudentResponse


async def create_student(student: StudentCreate) -> StudentResponse:
    """Create a new student"""
    db = await get_database()
    
    # Check if email already exists
    existing_student = await db.students.find_one({"email": student.email})
    if existing_student:
        raise ValueError("Student with this email already exists")
    
    student_data = student.model_dump()
    result = await db.students.insert_one(student_data)
    
    created_student = await db.students.find_one({"_id": result.inserted_id})
    return StudentResponse(
        id=str(created_student["_id"]),
        **{k: v for k, v in created_student.items() if k != "_id"}
    )


async def get_student_by_id(student_id: str) -> Optional[StudentResponse]:
    """Get student by ID"""
    db = await get_database()
    
    if not ObjectId.is_valid(student_id):
        return None
    
    student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return None
    
    return StudentResponse(
        id=str(student["_id"]),
        **{k: v for k, v in student.items() if k != "_id"}
    )


async def get_all_students() -> List[StudentResponse]:
    """Get all students"""
    db = await get_database()
    students = []
    
    async for student in db.students.find():
        students.append(StudentResponse(
            id=str(student["_id"]),
            **{k: v for k, v in student.items() if k != "_id"}
        ))
    
    return students


async def update_student(student_id: str, student_update: StudentUpdate) -> Optional[StudentResponse]:
    """Update student by ID"""
    db = await get_database()
    
    if not ObjectId.is_valid(student_id):
        return None
    
    # Check if student exists
    existing_student = await db.students.find_one({"_id": ObjectId(student_id)})
    if not existing_student:
        return None
    
    # Check if email already exists (if email is being updated)
    if student_update.email:
        email_exists = await db.students.find_one({
            "email": student_update.email,
            "_id": {"$ne": ObjectId(student_id)}
        })
        if email_exists:
            raise ValueError("Student with this email already exists")
    
    # Update only provided fields
    update_data = {k: v for k, v in student_update.model_dump().items() if v is not None}
    
    if not update_data:
        return await get_student_by_id(student_id)
    
    await db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": update_data}
    )
    
    return await get_student_by_id(student_id)


async def delete_student(student_id: str) -> bool:
    """Delete student by ID"""
    db = await get_database()
    
    if not ObjectId.is_valid(student_id):
        return False
    
    result = await db.students.delete_one({"_id": ObjectId(student_id)})
    return result.deleted_count > 0