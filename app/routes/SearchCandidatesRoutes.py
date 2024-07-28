from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from app.services import CandidateService
from app.middleware.Auth import get_current_user
from app.serializers.CandidateSerializers import CandidateResponse
from typing import Optional

router = APIRouter(prefix="/all-candidates", tags=["All Candidates"])

@router.get("/")
async def get_all_candidates(
    current_user: dict = Depends(get_current_user),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    career_level: Optional[str] = Query(None, description="Filter by career level"),
    job_major: Optional[str] = Query(None, description="Filter by job major"),
    degree_type: Optional[str] = Query(None, description="Filter by degree type"),
    nationality: Optional[str] = Query(None, description="Filter by nationality"),
    city: Optional[str] = Query(None, description="Filter by city"),
    keywords: Optional[str] = Query(None, description="Search across multiple fields")
):

    query_params = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "career_level": career_level,
        "job_major": job_major,
        "degree_type": degree_type,
        "nationality": nationality,
        "city": city,
        "keywords": keywords
    }

    candidates = await CandidateService.search_candidates(query_params)
    
    if not candidates:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No candidates found")
    
    candidate_responses = [CandidateResponse.map(candidate).model_dump() for candidate in candidates]
    return JSONResponse(content={"data": candidate_responses}, status_code=status.HTTP_200_OK)