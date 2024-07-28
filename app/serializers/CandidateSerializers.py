from pydantic import BaseModel, ConfigDict
from typing import List, Dict
from bson import ObjectId

class CandidateResponse(BaseModel):
    first_name: str
    last_name: str
    email: str
    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: List[str]
    nationality: str
    city: str
    salary: float
    gender: str

    # class Config:
    #     json_encoders = {
    #         ObjectId: str
    #     }

    model_config = ConfigDict(json_encoders={ObjectId: str})

    @classmethod
    def map(cls, candidate: Dict[str, any]) -> 'CandidateResponse':
        """
        Maps candidate data to the CandidateResponse format.
        
        Args:
            candidate (Dict[str, Any]): The candidate data from the database.

        Returns:
            CandidateResponse: An instance of CandidateResponse with mapped data.
        """
        return cls(
            first_name=candidate['first_name'],
            last_name=candidate['last_name'],
            email=candidate['email'],
            career_level=candidate['career_level'],
            job_major=candidate['job_major'],
            years_of_experience=candidate['years_of_experience'],
            degree_type=candidate['degree_type'],
            skills=candidate['skills'],
            nationality=candidate['nationality'],
            city=candidate['city'],
            salary=candidate['salary'],
            gender=candidate['gender']
        )