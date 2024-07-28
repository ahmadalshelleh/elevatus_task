from pydantic import BaseModel, EmailStr
from uuid import uuid4
from typing import List, Literal, Optional

class Candidate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    uuid: Optional[str] = None  # UUID will be generated server-side
    career_level: Literal['Junior', 'Mid Level', 'Senior']
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: List[str]
    nationality: str
    city: str
    salary: float
    gender: Literal['Male', 'Female', 'Not Specified']

    def __init__(self, **data):
        super().__init__(**data)
        if self.uuid is None:
            self.uuid = str(uuid4())