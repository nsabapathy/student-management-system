#!/usr/bin/env python3
"""
Script to create a test user in the MongoDB database
"""
import asyncio
import sys
from app.database import get_database
from app.models.auth import UserCreate
from app.services.auth import create_user

async def main():
    try:
        # Create test user
        user = UserCreate(
            username="naveensa",
            email="naveensa@example.com",
            password="password123"  # You can change this password
        )
        
        # Try to create user
        try:
            created_user = await create_user(user)
            print(f"User created successfully: {created_user.username}")
        except ValueError as e:
            print(f"User already exists: {e}")
            
            # If user exists, let's update the password
            db = await get_database()
            from app.utils.password import hash_password
            hashed_password = hash_password("password123")  # You can change this password
            
            # Update user's password
            result = await db.users.update_one(
                {"username": "naveensa"},
                {"$set": {"hashed_password": hashed_password}}
            )
            
            if result.modified_count:
                print("Password updated successfully")
            else:
                print("Failed to update password")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
