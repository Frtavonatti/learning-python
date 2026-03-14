"""
Tests for user endpoints.
"""
import pytest


class TestCreateUser:
    """Tests for creating users."""
    
    def test_create_user_success(self, client, sample_user_data):
        """Test successful user creation."""
        response = client.post("/users/", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["username"] == sample_user_data["username"]
        assert "id" in data
        assert "created_at" in data
        assert "hashed_password" not in data  # Password should not be returned
    
    def test_create_user_duplicate_email(self, client, sample_user_data):
        """Test creating user with duplicate email fails."""
        # Create first user
        client.post("/users/", json=sample_user_data)
        
        # Try to create another user with same email
        duplicate_user = sample_user_data.copy()
        duplicate_user["username"] = "different_username"
        response = client.post("/users/", json=duplicate_user)
        
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_create_user_duplicate_username(self, client, sample_user_data):
        """Test creating user with duplicate username fails."""
        # Create first user
        client.post("/users/", json=sample_user_data)
        
        # Try to create another user with same username
        duplicate_user = sample_user_data.copy()
        duplicate_user["email"] = "different@example.com"
        response = client.post("/users/", json=duplicate_user)
        
        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]
    
    def test_create_user_invalid_email(self, client, sample_user_data):
        """Test creating user with invalid email fails."""
        sample_user_data["email"] = "invalid-email"
        response = client.post("/users/", json=sample_user_data)
        
        assert response.status_code == 422  # Validation error


class TestGetUsers:
    """Tests for getting users."""
    
    def test_get_all_users_empty(self, client):
        """Test getting users when database is empty."""
        response = client.get("/users/")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_all_users(self, client, create_test_user):
        """Test getting all users."""
        response = client.get("/users/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["email"] == create_test_user["email"]
    
    def test_get_user_by_id(self, client, create_test_user):
        """Test getting a specific user by ID."""
        user_id = create_test_user["id"]
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == create_test_user["email"]
    
    def test_get_user_not_found(self, client):
        """Test getting a non-existent user."""
        response = client.get("/users/999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateUser:
    """Tests for updating users."""
    
    def test_update_user_success(self, client, create_test_user):
        """Test successful user update."""
        user_id = create_test_user["id"]
        update_data = {
            "email": "updated@example.com",
            "username": "updateduser",
            "password": "newpassword123",
            "roles": ["user", "admin"]
        }
        
        response = client.put(f"/users/{user_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == update_data["email"]
        assert data["username"] == update_data["username"]
    
    def test_update_user_not_found(self, client):
        """Test updating a non-existent user."""
        update_data = {
            "email": "updated@example.com",
            "username": "updateduser",
            "password": "newpassword123",
            "roles": ["user"]
        }
        
        response = client.put("/users/999", json=update_data)
        
        assert response.status_code == 404


class TestDeleteUser:
    """Tests for deleting users."""
    
    def test_delete_user_success(self, client, create_test_user):
        """Test successful user deletion."""
        user_id = create_test_user["id"]
        
        response = client.delete(f"/users/{user_id}")
        
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self, client):
        """Test deleting a non-existent user."""
        response = client.delete("/users/999")
        
        assert response.status_code == 404
