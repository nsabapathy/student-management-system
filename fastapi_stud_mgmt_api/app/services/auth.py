from typing import Optional
from app.database import get_database
from app.models.auth import User, UserCreate
from app.schemas.user import UserInDB
from app.utils.password import hash_password, verify_password
from bson import ObjectId


async def create_user(user: UserCreate) -> User:
    """Create a new user"""
    db = await get_database()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        raise ValueError("Username already exists")
    
    existing_email = await db.users.find_one({"email": user.email})
    if existing_email:
        raise ValueError("Email already exists")
    
    # Hash password and create user
    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_active": True
    }
    
    result = await db.users.insert_one(user_data)
    
    return User(
        id=str(result.inserted_id),
        username=user.username,
        email=user.email,
        is_active=True
    )


async def authenticate_user(username: str, password: str) -> Optional[User]:
    """Authenticate user with username and password"""
    db = await get_database()
    user_data = await db.users.find_one({"username": username})
    
    if not user_data:
        return None
    
    if not verify_password(password, user_data["hashed_password"]):
        return None
    
    return User(
        id=str(user_data["_id"]),
        username=user_data["username"],
        email=user_data["email"],
        is_active=user_data["is_active"]
    )


async def get_user_by_username(username: str) -> Optional[User]:
    """Get user by username"""
    db = await get_database()
    user_data = await db.users.find_one({"username": username})
    
    if not user_data:
        return None
    
    return User(
        id=str(user_data["_id"]),
        username=user_data["username"],
        email=user_data["email"],
        is_active=user_data["is_active"]
        )