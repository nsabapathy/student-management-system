#!/usr/bin/env python3
"""
Script to test password verification
"""
from app.utils.password import verify_password
from pymongo import MongoClient
import os

# Use the correct MongoDB URI for Docker
mongo_uri = os.getenv("MONGODB_URI", "mongodb://mongodb2:27017")
db_name = os.getenv("DATABASE_NAME", "student_management")

def main():
    # Connect to MongoDB
    print(f"Attempting to connect to MongoDB at {mongo_uri}...")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    print(f"Successfully connected to MongoDB at {mongo_uri}")
    
    # Get the user data
    username = "naveensa"
    user_data = db.users.find_one({"username": username})
    
    if not user_data:
        print(f"User {username} not found in the database!")
        return 1
    
    print(f"Found user: {username}")
    print(f"Stored hashed password: {user_data['hashed_password']}")
    
    # Test different passwords
    test_passwords = ["password123", "admin", "naveensa", "123456"]
    
    for password in test_passwords:
        result = verify_password(password, user_data["hashed_password"])
        print(f"Testing password '{password}': {'✅ Success' if result else '❌ Failed'}")
    
    return 0

if __name__ == "__main__":
    exit(main())
