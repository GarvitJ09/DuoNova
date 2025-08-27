from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        # Optionally test connection
        await self.client.admin.command('ping')
        return self.db

    async def close(self):
        if self.client:
            self.client.close()

mongodb = MongoDB()
