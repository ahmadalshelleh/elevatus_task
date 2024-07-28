from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import FileResponse
from datetime import datetime
import csv
from app.services import CandidateService

router = APIRouter(prefix="/generate-report", tags=["Report"])

@router.get("/")
async def generate_report(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format")
):
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    
    candidates = await CandidateService.get_all_candidates(start_date, end_date)

    csv_file_path = "candidates_report.csv"
    
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow([
            "UUID", "First Name", "Last Name", "Email", "Career Level", 
            "Job Major", "Years of Experience", "Degree Type", 
            "Skills", "Nationality", "City", "Salary", "Gender"
        ])

        for candidate in candidates:
            writer.writerow([
                candidate["uuid"], candidate["first_name"], candidate["last_name"], 
                candidate["email"], candidate["career_level"], candidate["job_major"], 
                candidate["years_of_experience"], candidate["degree_type"], 
                ", ".join(candidate["skills"]), candidate["nationality"], 
                candidate["city"], candidate["salary"], candidate["gender"]
            ])
    
    return FileResponse(
        path=csv_file_path,
        media_type='text/csv',
        filename='candidates_report.csv'
    )