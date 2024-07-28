from fastapi import Header, HTTPException, status
from typing import Optional
from app.repositories import UserRepository

async def get_current_user(x_user_uuid: Optional[str] = Header(None, alias="X-User-UUID")) -> dict:
    if not x_user_uuid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing UUID in headers",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = UserRepository.get_user_by_uuid(x_user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user