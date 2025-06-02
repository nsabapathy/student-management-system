#!/usr/bin/env python3
"""
Script to create a test user in the MongoDB database
"""
import pymongo
from pymongo import MongoClient
import os
import secrets
import base64
from passlib.context import CryptContext

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Use the correct MongoDB URI for Docker
mongo_uri = os.getenv("MONGODB_URI", "mongodb://mongodb2:27017")
db_name = os.getenv("DATABASE_NAME", "student_management")

def main():
    try:
        # Connect to MongoDB
        print(f"Attempting to connect to MongoDB at {mongo_uri}...")
        client = MongoClient(mongo_uri)
        # Test the connection
        client.admin.command('ping')
        db = client[db_name]
        print(f"Successfully connected to MongoDB at {mongo_uri}")
        
        # Check if user exists
        username = "naveensa"
        user = db.users.find_one({"username": username})
        
        if user:
            print(f"User {username} already exists. Updating password...")
            # Update password
            hashed_password = hash_password("password123")
            result = db.users.update_one(
                {"username": username},
                {"$set": {"hashed_password": hashed_password}}
            )
            print(f"Password updated: {result.modified_count} document(s) modified")
        else:
            print(f"Creating new user {username}...")
            # Create new user
            hashed_password = hash_password("password123")
            user_data = {
                "username": username,
                "email": f"{username}@example.com",
                "hashed_password": hashed_password,
                "is_active": True
            }
            result = db.users.insert_one(user_data)
            print(f"User created with ID: {result.inserted_id}")
            
        # Verify user exists
        user = db.users.find_one({"username": username})
        if user:
            print(f"User {username} exists in the database!")
        else:
            print(f"User {username} does not exist in the database!")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
