from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)

try:
    # Test MongoDB connection
    server_info = client.server_info()
    print("✅ MongoDB is connected!")
    print("📌 MongoDB Version:", server_info["version"])

    # List available databases
    databases = client.list_database_names()
    print("📂 Available Databases:", databases)

    # Exclude system databases
    system_dbs = ["admin", "config", "local"]
    user_databases = [db for db in databases if db not in system_dbs]

    if user_databases:
        db_name = user_databases[0]  # Select the first user-created database
        db = client[db_name]
        collection_names = db.list_collection_names()
        print(f"📁 Using `{db_name}` database.")
        print(f"📂 Collections in `{db_name}`:", collection_names)

        # Check if 'documents' collection exists
        if "documents" in collection_names:
            documents_collection = db["documents"]
        else:
            print("⚠ `documents` collection not found! Creating it now...")
            db.create_collection("documents")
            documents_collection = db["documents"]
    else:
        print("⚠ No user databases found! Creating `documentDB`...")
        db = client["documentDB"]
        db.create_collection("documents")
        documents_collection = db["documents"]
        print("✅ `documentDB` and `documents` collection created.")

except Exception as e:
    print("❌ MongoDB Connection Failed:", e)
    documents_collection = None  # Avoid errors in search.py if connection fails
