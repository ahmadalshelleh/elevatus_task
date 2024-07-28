import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.services import CandidateService
from app.serializers.CandidateSerializers import CandidateResponse
from bson import ObjectId
from fastapi import HTTPException

client = TestClient(app)

@pytest.fixture
def mock_current_user():
    return {
        "uuid": "f2bf23d7-3196-465b-9002-817e600d86fe",
    }

@pytest.fixture
def test_candidate():
    return {
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
    }

def test_create_candidate(mock_current_user, test_candidate):
    expected_candidate_id = "123e4567e89b12d3a456426614174001"

    with patch("app.middleware.Auth.get_current_user", return_value=mock_current_user):
        with patch.object(CandidateService, "create_candidate", return_value=expected_candidate_id):
            response = client.post("/candidate", json=test_candidate, headers={"X-User-UUID": mock_current_user["uuid"]})

    assert response.status_code == 201
    assert response.json() == {"data": {"candidate_id": expected_candidate_id}}

def test_create_candidate_unauthorized(test_candidate):
    response = client.post("/candidate", json=test_candidate)

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing UUID in headers"}


def test_get_candidate(mock_current_user, test_candidate):
    candidate_id = "123e4567e89b12d3a456426614174002"
    candidate_response = CandidateResponse.map(test_candidate)

    with patch("app.middleware.Auth.get_current_user", return_value=mock_current_user):
        with patch.object(CandidateService, "get_candidate", return_value=test_candidate):
            response = client.get(f"/candidate/{candidate_id}", headers={"X-User-UUID": mock_current_user["uuid"]})

        assert response.status_code == 200
        assert response.json() == {"data": candidate_response.model_dump()}


def test_update_candidate(test_candidate, mock_current_user):
    candidate_id = str(ObjectId()) 

    with patch("app.middleware.Auth.get_current_user", return_value=mock_current_user):
        response = client.put(f"/candidate/{candidate_id}", json=test_candidate, headers={"X-User-UUID": mock_current_user["uuid"]})

        assert response.status_code == 200
        assert response.json() == {"status": "Candidate Updated!"}

def test_update_candidate_unauthorized(test_candidate):
    candidate_id = str(ObjectId()) 

    response = client.put(f"/candidate/{candidate_id}", json=test_candidate)

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing UUID in headers"}

def test_update_candidate_not_found(test_candidate, mock_current_user):
    candidate_id = str(ObjectId()) 

    with patch("app.middleware.Auth.get_current_user", return_value=mock_current_user):
        with patch.object(CandidateService, "update_candidate", side_effect=HTTPException(status_code=404, detail="Candidate not found")):
            response = client.put(f"/candidate/{candidate_id}", json=test_candidate, headers={"X-User-UUID": mock_current_user["uuid"]})

            assert response.status_code == 404
            assert response.json() == {"detail": "Candidate not found"}


def test_delete_candidate(mock_current_user):
    candidate_id = str(ObjectId()) 

    with patch("app.middleware.Auth.get_current_user", return_value=mock_current_user):
        with patch("app.services.CandidateService.delete_candidate") as mock_delete:
            response = client.delete(f"/candidate/{candidate_id}", headers={"X-User-UUID": mock_current_user["uuid"]})

            assert response.status_code == 200
            assert response.json() == {"status": "Candidate Deleted!"}
            mock_delete.assert_called_once_with(candidate_id)