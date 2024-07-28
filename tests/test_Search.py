import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from bson import ObjectId
from app.main import app
from app.serializers.CandidateSerializers import CandidateResponse

client = TestClient(app)

@pytest.fixture
def mock_current_user():
    return {
        "uuid": "f2bf23d7-3196-465b-9002-817e600d86fe",
    }

@pytest.fixture
def test_candidate():
    return [{
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "career_level": "Mid Level",
        "job_major": "Computer Science",
        "years_of_experience": 5,
        "degree_type": "Bachelor",
        "skills": ["Python", "FastAPI"],
        "nationality": "American",
        "city": "New York",
        "salary": 80000,
        "gender": "Female"
    }]

def test_get_all_candidates_success(mock_current_user, test_candidate):
    with patch("app.middleware.Auth.get_current_user", return_value=mock_current_user):
        with patch("app.services.CandidateService.search_candidates", new_callable=AsyncMock) as mock_search_candidates:
            mock_search_candidates.return_value = test_candidate

            response = client.get("/all-candidates", headers={"X-User-UUID": mock_current_user["uuid"]})

            assert response.status_code == 200
            assert response.json() == {
                "data": [CandidateResponse.map(test_candidate[0]).model_dump()]
            }
            mock_search_candidates.assert_called_once()

def test_get_all_candidates_no_candidates(mock_current_user):
    with patch("app.middleware.Auth.get_current_user", return_value=mock_current_user):
        with patch("app.services.CandidateService.search_candidates", new_callable=AsyncMock) as mock_search_candidates:
            mock_search_candidates.return_value = []

            response = client.get("/all-candidates", headers={"X-User-UUID": mock_current_user["uuid"]})

            assert response.status_code == 404
            assert response.json() == {"detail": "No candidates found"}
            mock_search_candidates.assert_called_once()

def test_get_all_candidates_with_filters(mock_current_user, test_candidate):
    with patch("app.middleware.Auth.get_current_user", return_value=mock_current_user):
        with patch("app.services.CandidateService.search_candidates", new_callable=AsyncMock) as mock_search_candidates:
            mock_search_candidates.return_value = test_candidate

            response = client.get("/all-candidates", params={
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@example.com"
            }, headers={"X-User-UUID": mock_current_user["uuid"]})

            assert response.status_code == 200
            assert response.json() == {
                "data": [CandidateResponse.map(test_candidate[0]).model_dump()]
            }
            mock_search_candidates.assert_called_once()