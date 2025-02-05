from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return JSONResponse(content={"status": "OK"}, status_code=status.HTTP_200_OK)