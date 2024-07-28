from app.models.User import User
from app.repositories import UserRepository

@staticmethod
def create_user(user: User):
    return UserRepository.create_user(user)

@staticmethod
async def get_user(user_id: str):
    return UserRepository.get_user(user_id)

def update_user(user_id: str, user: User):
    UserRepository.update_user(user_id, user)

def delete_user(user_id: str):
    UserRepository.delete_user(user_id)