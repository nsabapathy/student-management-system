from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.student import StudentCreate, StudentUpdate, StudentResponse
from app.models.auth import User
from app.services.student import (
    create_student,
    get_student_by_id,
    get_all_students,
    update_student,
    delete_student
)
from app.middleware.auth import get_current_active_user

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_new_student(
    student: StudentCreate,
    current_user: User = Depends(get_current_active_user)
):
    """Create a new student"""
    try:
        created_student = await create_student(student)
        return created_student
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[StudentResponse])
async def get_students(current_user: User = Depends(get_current_active_user)):
    """Get all students"""
    students = await get_all_students()
    return students


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get student by ID"""
    student = await get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student


@router.put("/{student_id}", response_model=StudentResponse)
async def update_existing_student(
    student_id: str,
    student_update: StudentUpdate,
    current_user: User = Depends(get_current_active_user)
):
    """Update student by ID"""
    try:
        updated_student = await update_student(student_id, student_update)
        if not updated_student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return updated_student
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_student(
    student_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Delete student by ID"""
    deleted = await delete_student(student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return None