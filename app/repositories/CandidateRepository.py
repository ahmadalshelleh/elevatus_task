from singleton.mongodb import get_database
from app.models.Candidate import Candidate
from bson import ObjectId
from typing import List


db = get_database()
candidates_collection = db.get_collection("candidates")

def create_candidate(candidate: Candidate):
    candidate_dict = candidate.model_dump()
    result = candidates_collection.insert_one(candidate_dict)
    return str(result.inserted_id)

def get_candidate(candidate_id: str):
    candidate = candidates_collection.find_one({"_id": ObjectId(candidate_id)})
    return candidate

def update_candidate(candidate_id: str, candidate: Candidate):
    candidate_dict = candidate.model_dump()
    candidates_collection.update_one({"_id": ObjectId(candidate_id)}, {"$set": candidate_dict})

def delete_candidate(candidate_id: str):
    candidates_collection.delete_one({"_id": ObjectId(candidate_id)})

async def get_all_candidates(start_oid: ObjectId, end_oid: ObjectId) -> List[dict]:
    query = {"_id": {"$gte": start_oid, "$lt": end_oid}}
    cursor = candidates_collection.find(query)
    candidates = list(cursor)
    return candidates

async def search_candidates(query_params: dict) -> List[dict]:
    search_query = {}

    for key, value in query_params.items():
        if value is not None:
            if key in ["first_name", "last_name", "email", "career_level", "job_major", "degree_type", "nationality", "city"]:
                if isinstance(value, str):
                    search_query[key] = {"$regex": value, "$options": "i"}
            elif key == "keywords" and isinstance(value, str):
                search_query["$or"] = [
                    {"first_name": {"$regex": value, "$options": "i"}},
                    {"last_name": {"$regex": value, "$options": "i"}},
                    {"email": {"$regex": value, "$options": "i"}},
                    {"career_level": {"$regex": value, "$options": "i"}},
                    {"job_major": {"$regex": value, "$options": "i"}},
                    {"degree_type": {"$regex": value, "$options": "i"}},
                    {"nationality": {"$regex": value, "$options": "i"}},
                    {"city": {"$regex": value, "$options": "i"}}
                ]
    
    cursor = candidates_collection.find(search_query)
    candidates = list(cursor)
    return candidates