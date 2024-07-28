from bson import ObjectId
from datetime import datetime
from app.models.Candidate import Candidate
from app.repositories import CandidateRepository

def create_candidate(candidate: Candidate):
    return CandidateRepository.create_candidate(candidate)

@staticmethod
async def get_candidate(candidate_id: str):
    return CandidateRepository.get_candidate(candidate_id)

def update_candidate(candidate_id: str, candidate: Candidate):
    CandidateRepository.update_candidate(candidate_id, candidate)

def delete_candidate(candidate_id: str):
    CandidateRepository.delete_candidate(candidate_id)

def get_all_candidates(start_date: datetime, end_date: datetime):
    start_oid = ObjectId.from_datetime(start_date)
    end_oid = ObjectId.from_datetime(end_date)
    return CandidateRepository.get_all_candidates(start_oid, end_oid)

def search_candidates(search: object):
    return CandidateRepository.search_candidates(search)