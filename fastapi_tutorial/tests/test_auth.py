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
        """Test successful login returns JWT tokens."""
        client.post(self.register_url, json=sample_user_data)

        login_data = {
            "email": sample_user_data["email"],
            "password": sample_user_data["password"],
        }
        response = client.post(self.login_url, json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0

    def test_login_user_not_found(self, client):
        """Test login with non-existent user returns 404."""
        response = client.post(
            self.login_url,
            json={"email": "noone@example.com", "password": "any"},
        )
        assert response.status_code == 404

    def test_with_incorrect_password_fails(self, client, sample_user_data):
        client.post(self.register_url, json=sample_user_data)

        login_data = {
            "email": sample_user_data["email"],
            "password": "wrong_password",
        }
        response = client.post(self.login_url, json=login_data)

        assert response.status_code == 401


class TestRefreshToken:
    """Tests for the refresh token endpoint."""

    register_url = "/auth/register"
    login_url = "/auth/login"
    refresh_url = "/auth/refresh"

    def _login(self, client, sample_user_data) -> dict:
        client.post(self.register_url, json=sample_user_data)
        response = client.post(
            self.login_url,
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"],
            },
        )
        return response.json()

    def test_refresh_returns_new_tokens(self, client, sample_user_data):
        """Valid refresh token returns a new token pair."""
        tokens = self._login(client, sample_user_data)
        response = client.post(
            self.refresh_url, json={"refresh_token": tokens["refresh_token"]}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_with_access_token_fails(self, client, sample_user_data):
        """Sending an access token to /refresh must be rejected."""
        tokens = self._login(client, sample_user_data)
        response = client.post(
            self.refresh_url, json={"refresh_token": tokens["access_token"]}
        )

        assert response.status_code == 401

    def test_refresh_with_invalid_token_fails(self, client):
        """Garbage token returns 401."""
        response = client.post(
            self.refresh_url, json={"refresh_token": "not.a.valid.token"}
        )
        assert response.status_code == 401