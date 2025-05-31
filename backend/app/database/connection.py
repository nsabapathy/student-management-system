from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect_db(cls):
        cls.client = AsyncIOMotorClient(settings.mongodb_url)
        cls.db = cls.client[settings.database_name]
        print(f"Connected to MongoDB at: {settings.mongodb_url}")

    @classmethod
    async def close_db(cls):
        if cls.client is not None:
            cls.client.close()
            print("MongoDB connection closed.")

    @classmethod
    def get_db(cls):
        return cls.db

db = Database()
