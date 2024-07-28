from pydantic import BaseModel, EmailStr
from uuid import uuid4
from typing import Optional

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    uuid: Optional[str] = None  # UUID will be generated server-side

    def __init__(self, **data):
        super().__init__(**data)
        if self.uuid is None:
            self.uuid = str(uuid4())