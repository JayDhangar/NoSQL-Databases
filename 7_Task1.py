from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("mongodb_uri")

client = MongoClient(uri)

db = client["test_database"]
collection = db["users"]

collection.insert_one({"name": "Jay", "role": "Developer"})

for doc in collection.find():
    print(doc)