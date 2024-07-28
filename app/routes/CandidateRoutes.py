from fastapi import APIRouter, HTTPException, status, Depends, Query
from fastapi.responses import JSONResponse
from app.models.Candidate import Candidate
from app.services import CandidateService
from app.serializers.CandidateSerializers import CandidateResponse
from app.middleware.Auth import get_current_user

router = APIRouter(prefix="/candidate", tags=["Candidate"])

@router.post("/")
async def create_candidate(candidate: Candidate, current_user: dict = Depends(get_current_user)):
    candidate_id = CandidateService.create_candidate(candidate)
    return JSONResponse(content={"data": {"candidate_id": candidate_id}}, status_code=status.HTTP_201_CREATED)

@router.get("/{candidate_id}")
async def get_candidate(candidate_id: str, current_user: dict = Depends(get_current_user)):
    candidate = await CandidateService.get_candidate(candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return JSONResponse(content={"data": (CandidateResponse.map(candidate)).model_dump()}, status_code=status.HTTP_200_OK)

@router.put("/{candidate_id}")
def update_candidate(candidate_id: str, candidate: Candidate, current_user: dict = Depends(get_current_user)):
    CandidateService.update_candidate(candidate_id, candidate)
    return JSONResponse(content={"status": "Candidate Updated!"}, status_code=status.HTTP_200_OK)

@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: str, current_user: dict = Depends(get_current_user)):
    CandidateService.delete_candidate(candidate_id)
    return JSONResponse(content={"status": "Candidate Deleted!"}, status_code=status.HTTP_200_OK)