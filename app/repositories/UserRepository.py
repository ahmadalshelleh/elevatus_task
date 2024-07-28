from singleton.mongodb import get_database
from app.models.User import User
from bson import ObjectId

db = get_database()
users_collection = db.get_collection("users")

def create_user(user: User):
    user_dict = user.model_dump()
    result = users_collection.insert_one(user_dict)
    return str(result.inserted_id)

def get_user(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    return user

def update_user(user_id: str, user: User):
    user_dict = user.model_dump()
    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})

def delete_user(user_id: str):
    users_collection.delete_one({"_id": ObjectId(user_id)})

def get_user_by_uuid(uuid: str):
    return users_collection.find_one({"uuid": uuid})