from pymongo import MongoClient
from typing import Optional

class MongoDB:
    _instance: Optional[MongoClient] = None

    @classmethod
    def get_client(cls) -> MongoClient:
        if cls._instance is None:
            cls._instance = MongoClient("mongodb://localhost:27017")
        return cls._instance

    @classmethod
    def close_client(cls) -> None:
        if cls._instance:
            cls._instance.close()
            cls._instance = None

# Dependency
def get_database():
    client = MongoDB.get_client()
    return client.elevatus