import pytest


class TestCreateUser:
    """Tests for creating users."""

    register_url = "/auth/register"

    def test_create_user_success(self, client, sample_user_data):
        """Test successful user creation."""
        response = client.post(self.register_url, json=sample_user_data)

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
        client.post(self.register_url, json=sample_user_data)

        # Try to create another user with same email
        duplicate_user = sample_user_data.copy()
        duplicate_user["username"] = "different_username"
        response = client.post(self.register_url, json=duplicate_user)

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_create_user_duplicate_username(self, client, sample_user_data):
        """Test creating user with duplicate username fails."""
        # Create first user
        client.post(self.register_url, json=sample_user_data)

        # Try to create another user with same username
        duplicate_user = sample_user_data.copy()
        duplicate_user["email"] = "different@example.com"
        response = client.post(self.register_url, json=duplicate_user)

        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_create_user_invalid_email(self, client, sample_user_data):
        """Test creating user with invalid email fails."""
        sample_user_data["email"] = "invalid-email"
        response = client.post(self.register_url, json=sample_user_data)

        assert response.status_code == 422  # Validation error


class TestLoginUser:
    """Test for loging in"""

    login_url = "/auth/login"
    register_url = "/auth/register"

    def test_login_user_success(self, client, sample_user_data):
        """Test successful loging in"""
        # First register the user
        client.post(self.register_url, json=sample_user_data)

        # Then try to login with email (not username)
        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = client.post(self.login_url, json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Login successful"
        assert "user_id" in data
