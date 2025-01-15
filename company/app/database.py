from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_configuration

# MongoDB connection details
# MONGO_URI = "mongodb://localhost:27017"
# DATABASE_NAME = "company_db"
# COLLECTION_NAME = "companies"

config = get_configuration(["COMPANY_MONGO_URI", "COMPANY_DATABASE_NAME", "COMPANY_COLLECTION_NAME"])

client = AsyncIOMotorClient(config['COMPANY_MONGO_URI'])
db = client[config['COMPANY_DATABASE_NAME']]
collection = db[config['COMPANY_COLLECTION_NAME']]