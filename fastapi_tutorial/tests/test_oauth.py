"""
Tests for GitHub OAuth flow.

Strategy: the external GitHub HTTP calls (authorize_redirect,
authorize_access_token, get) are patched with AsyncMock / MagicMock so the
tests never hit the network.  The rest of the flow (DB lookup / creation,
token generation) runs against the real in-memory SQLite test database.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.responses import RedirectResponse

from app import models
from app.core.security import hash_password


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_get_side_effect(github_id: int = 123456, login: str = "githubuser"):
    """
    Returns a side_effect callable for the two sequential oauth.github.get()
    calls made inside github_callback:
      1st call → GET /user  (profile)
      2nd call → GET /user/emails
    """
    profile_resp = MagicMock()
    profile_resp.json.return_value = {"id": github_id, "login": login}

    emails_resp = MagicMock()
    emails_resp.json.return_value = [
        {"email": "oauth@example.com", "primary": True, "verified": True}
    ]

    responses = iter([profile_resp, emails_resp])

    async def _get(*args, **kwargs):
        return next(responses)

    return _get


def _make_get_no_email_side_effect():
    """Side effect that returns an empty verified-email list."""
    profile_resp = MagicMock()
    profile_resp.json.return_value = {"id": 999, "login": "noemail"}

    emails_resp = MagicMock()
    emails_resp.json.return_value = []  # no verified primary email

    responses = iter([profile_resp, emails_resp])

    async def _get(*args, **kwargs):
        return next(responses)

    return _get


# ---------------------------------------------------------------------------
# Test class
# ---------------------------------------------------------------------------

class TestGithubOAuth:
    login_url = "/auth/github"
    callback_url = "/auth/github/callback"

    # ------------------------------------------------------------------
    # Login redirect
    # ------------------------------------------------------------------

    def test_github_login_redirects(self, client):
        """GET /auth/github should redirect to GitHub's authorize URL."""
        with patch(
            "app.routers.oauth.oauth.github.authorize_redirect",
            new_callable=AsyncMock,
            return_value=RedirectResponse(
                url="https://github.com/login/oauth/authorize?client_id=test"
            ),
        ):
            # TestClient follows redirects by default; disable to inspect it
            response = client.get(self.login_url, follow_redirects=False)

        assert response.status_code in (302, 307)
        assert "github.com" in response.headers["location"]

    # ------------------------------------------------------------------
    # Callback — new user
    # ------------------------------------------------------------------

    def test_callback_creates_new_user(self, client, db_session):
        """A GitHub user with a new email gets registered and receives tokens."""
        with (
            patch(
                "app.routers.oauth.oauth.github.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "gh_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=_make_get_side_effect(github_id=123456, login="githubuser"),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

        # User should be persisted in DB
        user = (
            db_session.query(models.User)
            .filter(models.User.oauth_provider_id == "123456")
            .first()
        )
        assert user is not None
        assert user.email == "oauth@example.com"
        assert user.username == "githubuser"
        assert user.oauth_providers == "github"
        assert user.hashed_password is None  # no local password

    # ------------------------------------------------------------------
    # Callback — existing OAuth user (login)
    # ------------------------------------------------------------------

    def test_callback_returns_existing_oauth_user(self, client, db_session):
        """A previously linked GitHub user gets tokens without creating a duplicate."""
        # Pre-create the linked user
        existing = models.User(
            email="oauth@example.com",
            username="githubuser",
            hashed_password=None,
            roles=[],
            oauth_providers="github",
            oauth_provider_id="123456",
        )
        db_session.add(existing)
        db_session.commit()
        db_session.refresh(existing)
        user_id = existing.id

        with (
            patch(
                "app.routers.oauth.oauth.github.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "gh_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=_make_get_side_effect(github_id=123456, login="githubuser"),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

        # No duplicate should be created
        users = (
            db_session.query(models.User)
            .filter(models.User.oauth_provider_id == "123456")
            .all()
        )
        assert len(users) == 1
        assert users[0].id == user_id

    # ------------------------------------------------------------------
    # Callback — links to existing local account with same email
    # ------------------------------------------------------------------

    def test_callback_links_existing_local_account(self, client, db_session):
        """
        If the GitHub email matches an already-registered local account,
        the account gets linked instead of creating a duplicate.
        """
        # Pre-create a local user with the same email that GitHub will return
        local_user = models.User(
            email="oauth@example.com",
            username="localuser",
            hashed_password=hash_password("localpass"),
            roles=["user"],
            oauth_providers=None,
            oauth_provider_id=None,
        )
        db_session.add(local_user)
        db_session.commit()
        db_session.refresh(local_user)
        local_id = local_user.id

        with (
            patch(
                "app.routers.oauth.oauth.github.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "gh_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=_make_get_side_effect(github_id=777, login="githubuser"),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 200

        # Reload the user from DB
        db_session.expire_all()
        updated = db_session.query(models.User).filter(models.User.id == local_id).first()
        assert updated.oauth_providers == "github"
        assert updated.oauth_provider_id == "777"

        # Still only one user with that email
        count = db_session.query(models.User).filter(models.User.email == "oauth@example.com").count()
        assert count == 1

    # ------------------------------------------------------------------
    # Callback — username conflict → suffix added
    # ------------------------------------------------------------------

    def test_callback_username_conflict_adds_suffix(self, client, db_session):
        """
        If the GitHub login is already taken, a numeric suffix is appended
        until a unique username is found.
        """
        # Occupy the base username
        existing = models.User(
            email="other@example.com",
            username="githubuser",
            hashed_password=hash_password("pass"),
            roles=[],
        )
        db_session.add(existing)
        db_session.commit()

        with (
            patch(
                "app.routers.oauth.oauth.github.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "gh_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=_make_get_side_effect(github_id=999, login="githubuser"),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 200

        new_user = (
            db_session.query(models.User)
            .filter(models.User.oauth_provider_id == "999")
            .first()
        )
        assert new_user is not None
        assert new_user.username == "githubuser_1"

    # ------------------------------------------------------------------
    # Callback — no verified email → 400
    # ------------------------------------------------------------------

    def test_callback_no_verified_email_returns_400(self, client):
        """If GitHub returns no verified primary email, respond with 400."""
        with (
            patch(
                "app.routers.oauth.oauth.github.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "gh_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=_make_get_no_email_side_effect(),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 400
        assert "verified" in response.json()["detail"].lower() or "email" in response.json()["detail"].lower()
