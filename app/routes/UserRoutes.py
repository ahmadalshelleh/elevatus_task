from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.User import User
from app.services import UserService
from app.serializers.UserSerializers import UserResponse

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/")
def create_user(user: User):
    user_id = UserService.create_user(user)
    return JSONResponse(content={"data": {"user_id": user_id}}, status_code=status.HTTP_201_CREATED)

@router.get("/{user_id}")
async def get_user(user_id: str):
    user = await UserService.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={"data": (UserResponse.map(user)).model_dump()}, status_code=status.HTTP_200_OK)

@router.put("/{user_id}")
def update_user(user_id: str, user: User):
    UserService.update_user(user_id, user)
    return JSONResponse(content={"status": "User Updated!"}, status_code=status.HTTP_200_OK)

@router.delete("/{user_id}")
def delete_user(user_id: str):
    UserService.delete_user(user_id)
    return JSONResponse(content={"status": "User Deleted!"}, status_code=status.HTTP_200_OK)