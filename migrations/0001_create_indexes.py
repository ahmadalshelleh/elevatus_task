from singleton.mongodb import get_database
from pymongo import ASCENDING

db = get_database()
users_collection = db.get_collection("users")

def create_indexes():
    users_collection.create_index([("uuid", ASCENDING)], unique=True)
    
    print("Indexes created successfully")

if __name__ == "__main__":
    create_indexes()