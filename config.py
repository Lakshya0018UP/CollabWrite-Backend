import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")
cred_path=os.getenv("FIREBASE_CREDENTIALS_PATH")

# Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
client=AsyncIOMotorClient(uri)
db=client.collabWrite_data
user=db["data"]
documents=db["documents"]

