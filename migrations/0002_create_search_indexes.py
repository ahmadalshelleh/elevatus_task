from singleton.mongodb import get_database
from pymongo import TEXT
from pymongo.errors import OperationFailure

db = get_database()
candidates_collection = db.get_collection("candidates")

def create_indexes():
    candidates_collection.create_index([
        ("first_name", TEXT),
        ("last_name", TEXT),
        ("email", TEXT),
        ("career_level", TEXT),
        ("job_major", TEXT),
        ("degree_type", TEXT),
        ("nationality", TEXT),
        ("city", TEXT)
    ], name='search_fields_text')

    print("Indexes created successfully")

if __name__ == "__main__":
    create_indexes()