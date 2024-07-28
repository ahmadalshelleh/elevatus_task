import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
@patch("app.services.CandidateService.get_all_candidates", new_callable=AsyncMock)
async def test_generate_report_success(mock_get_all_candidates):
    # Mock data for the report
    mock_candidates = [
        {
            "uuid": "123e4567-e89b-12d3-a456-426614174000",
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "career_level": "Mid Level",
            "job_major": "Computer Science",
            "years_of_experience": 5,
            "degree_type": "Bachelor",
            "skills": ["Python", "FastAPI"],
            "nationality": "American",
            "city": "New York",
            "salary": 80000.0,
            "gender": "Female"
        }
    ]
    mock_get_all_candidates.return_value = mock_candidates

    response = client.get("/generate-report", params={"start_date": "2024-01-01", "end_date": "2024-12-31"})

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv; charset=utf-8"
    assert response.headers["Content-Disposition"].startswith("attachment; filename=")
    assert "candidates_report.csv" in response.headers["Content-Disposition"]
    assert response.content.startswith(b"UUID,First Name,Last Name,Email,Career Level,Job Major,Years of Experience,Degree Type,Skills,Nationality,City,Salary,Gender")
    assert b"123e4567-e89b-12d3-a456-426614174000" in response.content
    assert b"Jane" in response.content
    assert b"Doe" in response.content

@pytest.mark.asyncio
@patch("app.services.CandidateService.get_all_candidates", new_callable=AsyncMock)
async def test_generate_report_no_candidates(mock_get_all_candidates):
    mock_get_all_candidates.return_value = []

    response = client.get("/generate-report", params={"start_date": "2024-01-01", "end_date": "2024-12-31"})

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv; charset=utf-8"
    assert response.headers["Content-Disposition"].startswith("attachment; filename=")
    assert "candidates_report.csv" in response.headers["Content-Disposition"]
    assert b"UUID,First Name,Last Name,Email,Career Level,Job Major,Years of Experience,Degree Type,Skills,Nationality,City,Salary,Gender" in response.content
    assert b"123e4567-e89b-12d3-a456-426614174000" not in response.content

def test_generate_report_invalid_date_format():
    response = client.get("/generate-report", params={"start_date": "01-01-2024", "end_date": "2024-12-31"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid date format. Use YYYY-MM-DD."}