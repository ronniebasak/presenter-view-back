import motor.motor_asyncio
import os
DB = "gpresent"


client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_CONNECT'))
db = client[DB]
