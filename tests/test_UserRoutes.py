from fastapi.testclient import TestClient
from app.main import app
from bson import ObjectId
from app.services import UserService
from unittest.mock import patch
from app.serializers.UserSerializers import UserResponse

client = TestClient(app)

def test_create_user():
    test_user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }
    
    expected_user_id = "123e4567e89b12d3a456426614174000"
    
    with patch.object(UserService, "create_user", return_value=expected_user_id):
        response = client.post("/user", json=test_user)
        
    assert response.status_code == 201
    assert response.json() == {"data": {"user_id": expected_user_id}}

def test_get_user():
    user_id = "123e4567e89b12d3a456426614174000"
    test_user = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }
    user_response = UserResponse.map(test_user)

    with patch.object(UserService, "get_user", return_value=test_user):
        response = client.get(f"/user/{user_id}")

    assert response.status_code == 200
    assert response.json() == {"data": user_response.model_dump()}

def test_update_user():
    user_id = str(ObjectId())  # Replace with a valid user ID for testing
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }
    response = client.put(f"/user/{user_id}", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"status": "User Updated!"}

def test_delete_user():
    user_id = str(ObjectId())  # Replace with a valid user ID for testing
    response = client.delete(f"/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"status": "User Deleted!"}