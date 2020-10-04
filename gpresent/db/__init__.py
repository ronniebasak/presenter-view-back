import motor.motor_asyncio
DB = "gpresent"


client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
db = client[DB]
