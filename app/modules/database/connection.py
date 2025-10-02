"""
MongoDB Connection Manager
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional

from app.config import settings


class MongoDBConnection:
    """Singleton MongoDB connection manager"""
    
    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        """
        Lấy MongoDB client (tạo mới nếu chưa có)
        
        Returns:
            AsyncIOMotorClient instance
        """
        if cls._client is None:
            cls._client = AsyncIOMotorClient(settings.mongodb_uri)
        return cls._client
    
    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """
        Lấy database instance
        
        Returns:
            AsyncIOMotorDatabase instance
        """
        if cls._database is None:
            client = cls.get_client()
            cls._database = client[settings.mongodb_database]
        return cls._database
    
    @classmethod
    async def close(cls):
        """Đóng kết nối MongoDB"""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._database = None


# Helper functions
def get_database() -> AsyncIOMotorDatabase:
    """
    Helper function để lấy database instance
    
    Returns:
        AsyncIOMotorDatabase instance
    """
    return MongoDBConnection.get_database()


async def close_database_connection():
    """Helper function để đóng kết nối database"""
    await MongoDBConnection.close()

