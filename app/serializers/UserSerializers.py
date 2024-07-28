from pydantic import BaseModel, EmailStr
from typing import Dict

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    @classmethod
    def map(cls, user: Dict[str, any]) -> 'UserResponse':
        return cls(
            first_name=user['first_name'],
            last_name=user['last_name'],
            email=user['email']
        )