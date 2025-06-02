#!/usr/bin/env python3
"""
Script to test authentication for a specific user
"""
import asyncio
from app.services.auth import authenticate_user

async def test_authentication(username: str, password: str):
    print(f"Testing authentication for user '{username}'...")
    user = await authenticate_user(username, password)
    
    if user:
        print(f"✅ Authentication successful for user: {user.username}")
        print(f"User details: ID={user.id}, Email={user.email}, Is Active={user.is_active}")
        return True
    else:
        print(f"❌ Authentication failed for user: {username}")
        return False
        
async def main():
    # Test authentication with naveensa user
    username = "naveensa"
    password = "password123"
    
    success = await test_authentication(username, password)
    
    if not success:
        # Try another common password
        print("\nTrying with another password...")
        await test_authentication(username, "admin")

if __name__ == "__main__":
    asyncio.run(main())
