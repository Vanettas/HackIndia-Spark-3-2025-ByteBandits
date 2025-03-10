from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["document_db"]
documents_collection = db["documents"]
