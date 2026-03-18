"""
Tests for GitHub and Google OAuth flows.

Strategy: the external OAuth HTTP calls (authorize_redirect,
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
        oauth_account = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.provider == "github",
                models.OAuthAccount.provider_user_id == "123456",
            )
            .first()
        )
        assert oauth_account is not None
        user = oauth_account.user
        assert user.email == "oauth@example.com"
        assert user.username == "githubuser"
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
        )
        db_session.add(existing)
        db_session.commit()
        db_session.refresh(existing)
        user_id = existing.id

        # Create OAuth account link
        oauth_account = models.OAuthAccount(
            user_id=existing.id,
            provider="github",
            provider_user_id="123456",
        )
        db_session.add(oauth_account)
        db_session.commit()

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
        oauth_accounts = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.provider == "github",
                models.OAuthAccount.provider_user_id == "123456",
            )
            .all()
        )
        assert len(oauth_accounts) == 1
        assert oauth_accounts[0].user_id == user_id

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

        # Check that OAuth account was created and linked
        oauth_account = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.user_id == local_id,
                models.OAuthAccount.provider == "github",
            )
            .first()
        )
        assert oauth_account is not None
        assert oauth_account.provider_user_id == "777"

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

        oauth_account = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.provider == "github",
                models.OAuthAccount.provider_user_id == "999",
            )
            .first()
        )
        assert oauth_account is not None
        new_user = oauth_account.user
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


# ---------------------------------------------------------------------------
# Google OAuth Helpers
# ---------------------------------------------------------------------------

def _make_google_get_side_effect(
    google_id: str = "987654321",
    email: str = "googleuser@example.com",
    name: str = "Google User",
    verified_email: bool = True,
):
    """
    Returns a side_effect callable for oauth.google.get() call
    made inside google_callback:
      GET /oauth2/v2/userinfo
    """
    userinfo_resp = MagicMock()
    userinfo_resp.json.return_value = {
        "id": google_id,
        "email": email,
        "verified_email": verified_email,
        "name": name,
        "given_name": name.split()[0] if name else "",
        "family_name": name.split()[-1] if name and len(name.split()) > 1 else "",
        "picture": "https://example.com/photo.jpg",
    }

    async def _get(*args, **kwargs):
        return userinfo_resp

    return _get


def _make_google_get_unverified_email_side_effect():
    """Side effect that returns an unverified email."""
    userinfo_resp = MagicMock()
    userinfo_resp.json.return_value = {
        "id": "999999",
        "email": "unverified@example.com",
        "verified_email": False,
        "name": "Unverified User",
    }

    async def _get(*args, **kwargs):
        return userinfo_resp

    return _get


def _make_google_get_no_email_side_effect():
    """Side effect that returns a profile with no email."""
    userinfo_resp = MagicMock()
    userinfo_resp.json.return_value = {
        "id": "888888",
        "name": "No Email User",
        # email field is missing
    }

    async def _get(*args, **kwargs):
        return userinfo_resp

    return _get


# ---------------------------------------------------------------------------
# Google OAuth Test Class
# ---------------------------------------------------------------------------

class TestGoogleOAuth:
    login_url = "/auth/google"
    callback_url = "/auth/google/callback"

    # ------------------------------------------------------------------
    # Login redirect
    # ------------------------------------------------------------------

    def test_google_login_redirects(self, client):
        """GET /auth/google should redirect to Google's authorize URL."""
        with patch(
            "app.routers.oauth.oauth.google.authorize_redirect",
            new_callable=AsyncMock,
            return_value=RedirectResponse(
                url="https://accounts.google.com/o/oauth2/v2/auth?client_id=test"
            ),
        ):
            response = client.get(self.login_url, follow_redirects=False)

        assert response.status_code in (302, 307)
        assert "google.com" in response.headers["location"]

    # ------------------------------------------------------------------
    # Callback — new user
    # ------------------------------------------------------------------

    def test_callback_creates_new_user(self, client, db_session):
        """A Google user with a new email gets registered and receives tokens."""
        with (
            patch(
                "app.routers.oauth.oauth.google.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "google_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.google.get",
                side_effect=_make_google_get_side_effect(
                    google_id="987654321",
                    email="googleuser@example.com",
                    name="Google User",
                ),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

        # User should be persisted in DB
        oauth_account = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.provider == "google",
                models.OAuthAccount.provider_user_id == "987654321",
            )
            .first()
        )
        assert oauth_account is not None
        user = oauth_account.user
        assert user.email == "googleuser@example.com"
        assert user.username == "googleuser"  # Derived from name
        assert user.hashed_password is None  # no local password

    # ------------------------------------------------------------------
    # Callback — existing OAuth user (login)
    # ------------------------------------------------------------------

    def test_callback_returns_existing_oauth_user(self, client, db_session):
        """A previously linked Google user gets tokens without creating a duplicate."""
        # Pre-create the linked user
        existing = models.User(
            email="googleuser@example.com",
            username="googleuser",
            hashed_password=None,
            roles=[],
        )
        db_session.add(existing)
        db_session.commit()
        db_session.refresh(existing)
        user_id = existing.id

        # Create OAuth account link
        oauth_account = models.OAuthAccount(
            user_id=existing.id,
            provider="google",
            provider_user_id="987654321",
        )
        db_session.add(oauth_account)
        db_session.commit()

        with (
            patch(
                "app.routers.oauth.oauth.google.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "google_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.google.get",
                side_effect=_make_google_get_side_effect(
                    google_id="987654321",
                    email="googleuser@example.com",
                ),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

        # No duplicate should be created
        oauth_accounts = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.provider == "google",
                models.OAuthAccount.provider_user_id == "987654321",
            )
            .all()
        )
        assert len(oauth_accounts) == 1
        assert oauth_accounts[0].user_id == user_id

    # ------------------------------------------------------------------
    # Callback — links to existing local account with same email
    # ------------------------------------------------------------------

    def test_callback_links_existing_local_account(self, client, db_session):
        """
        If the Google email matches an already-registered local account,
        the account gets linked instead of creating a duplicate.
        """
        # Pre-create a local user with the same email that Google will return
        local_user = models.User(
            email="googleuser@example.com",
            username="localuser",
            hashed_password=hash_password("localpass"),
            roles=["user"],
        )
        db_session.add(local_user)
        db_session.commit()
        db_session.refresh(local_user)
        local_id = local_user.id

        with (
            patch(
                "app.routers.oauth.oauth.google.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "google_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.google.get",
                side_effect=_make_google_get_side_effect(
                    google_id="555555",
                    email="googleuser@example.com",
                ),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 200

        # Check that OAuth account was created and linked
        oauth_account = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.user_id == local_id,
                models.OAuthAccount.provider == "google",
            )
            .first()
        )
        assert oauth_account is not None
        assert oauth_account.provider_user_id == "555555"

        # Still only one user with that email
        count = db_session.query(models.User).filter(models.User.email == "googleuser@example.com").count()
        assert count == 1

    # ------------------------------------------------------------------
    # Callback — username conflict → suffix added
    # ------------------------------------------------------------------

    def test_callback_username_conflict_adds_suffix(self, client, db_session):
        """
        If the Google-derived username is already taken, a numeric suffix is appended
        until a unique username is found.
        """
        # Occupy the base username
        existing = models.User(
            email="other@example.com",
            username="googleuser",
            hashed_password=hash_password("pass"),
            roles=[],
        )
        db_session.add(existing)
        db_session.commit()

        with (
            patch(
                "app.routers.oauth.oauth.google.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "google_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.google.get",
                side_effect=_make_google_get_side_effect(
                    google_id="444444",
                    email="new@example.com",
                    name="Google User",
                ),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 200

        oauth_account = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.provider == "google",
                models.OAuthAccount.provider_user_id == "444444",
            )
            .first()
        )
        assert oauth_account is not None
        new_user = oauth_account.user
        assert new_user.username == "googleuser_1"

    # ------------------------------------------------------------------
    # Callback — unverified email → 400
    # ------------------------------------------------------------------

    def test_callback_unverified_email_returns_400(self, client):
        """If Google returns an unverified email, respond with 400."""
        with (
            patch(
                "app.routers.oauth.oauth.google.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "google_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.google.get",
                side_effect=_make_google_get_unverified_email_side_effect(),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 400
        assert "verified" in response.json()["detail"].lower()

    # ------------------------------------------------------------------
    # Callback — no email → 400
    # ------------------------------------------------------------------

    def test_callback_no_email_returns_400(self, client):
        """If Google returns no email, respond with 400."""
        with (
            patch(
                "app.routers.oauth.oauth.google.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "google_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.google.get",
                side_effect=_make_google_get_no_email_side_effect(),
            ),
        ):
            response = client.get(self.callback_url)

        assert response.status_code == 400
        assert "email" in response.json()["detail"].lower()


# ---------------------------------------------------------------------------
# Multi-Provider Tests
# ---------------------------------------------------------------------------

class TestMultiProviderOAuth:
    """Tests for linking multiple OAuth providers to one user."""

    def test_user_can_link_both_github_and_google(self, client, db_session):
        """
        A user with an existing local account can link both GitHub and Google,
        and login with either provider.
        """
        # Create a local user
        local_user = models.User(
            email="multiuser@example.com",
            username="multiuser",
            hashed_password=hash_password("localpass"),
            roles=["user"],
        )
        db_session.add(local_user)
        db_session.commit()
        db_session.refresh(local_user)
        user_id = local_user.id

        # 1. Link GitHub
        with (
            patch(
                "app.routers.oauth.oauth.github.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "gh_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=_make_get_side_effect(
                    github_id=111111, login="multiuser"
                ),
            ),
        ):
            # Mock the email to match our local user
            def custom_get_side_effect():
                profile_resp = MagicMock()
                profile_resp.json.return_value = {"id": 111111, "login": "multiuser"}

                emails_resp = MagicMock()
                emails_resp.json.return_value = [
                    {"email": "multiuser@example.com", "primary": True, "verified": True}
                ]

                responses = iter([profile_resp, emails_resp])

                async def _get(*args, **kwargs):
                    return next(responses)

                return _get

            with patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=custom_get_side_effect(),
            ):
                response = client.get("/auth/github/callback")

        assert response.status_code == 200

        # 2. Link Google to the same user
        with (
            patch(
                "app.routers.oauth.oauth.google.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "google_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.google.get",
                side_effect=_make_google_get_side_effect(
                    google_id="222222",
                    email="multiuser@example.com",
                    name="Multi User",
                ),
            ),
        ):
            response = client.get("/auth/google/callback")

        assert response.status_code == 200

        # 3. Verify both OAuth accounts are linked to the same user
        db_session.expire_all()
        oauth_accounts = (
            db_session.query(models.OAuthAccount)
            .filter(models.OAuthAccount.user_id == user_id)
            .all()
        )

        assert len(oauth_accounts) == 2
        providers = {acc.provider for acc in oauth_accounts}
        assert providers == {"github", "google"}

        # 4. Verify both have correct provider IDs
        github_account = next(acc for acc in oauth_accounts if acc.provider == "github")
        google_account = next(acc for acc in oauth_accounts if acc.provider == "google")

        assert github_account.provider_user_id == "111111"
        assert google_account.provider_user_id == "222222"

        # 5. Verify still only one user in the database with that email
        user_count = (
            db_session.query(models.User)
            .filter(models.User.email == "multiuser@example.com")
            .count()
        )
        assert user_count == 1

    def test_user_cannot_link_same_provider_twice(self, client, db_session):
        """
        A user cannot link the same OAuth provider (GitHub) twice.
        The unique constraint should prevent this.
        """
        # Create a user with GitHub already linked
        user = models.User(
            email="test@example.com",
            username="testuser",
            hashed_password=None,
            roles=[],
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        oauth_account = models.OAuthAccount(
            user_id=user.id,
            provider="github",
            provider_user_id="12345",
        )
        db_session.add(oauth_account)
        db_session.commit()

        # Try to login again with the same GitHub account
        with (
            patch(
                "app.routers.oauth.oauth.github.authorize_access_token",
                new_callable=AsyncMock,
                return_value={"access_token": "gh_fake_token"},
            ),
            patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=_make_get_side_effect(github_id=12345, login="testuser"),
            ),
        ):
            # Should succeed without creating duplicate
            def custom_get_side_effect():
                profile_resp = MagicMock()
                profile_resp.json.return_value = {"id": 12345, "login": "testuser"}

                emails_resp = MagicMock()
                emails_resp.json.return_value = [
                    {"email": "test@example.com", "primary": True, "verified": True}
                ]

                responses = iter([profile_resp, emails_resp])

                async def _get(*args, **kwargs):
                    return next(responses)

                return _get

            with patch(
                "app.routers.oauth.oauth.github.get",
                side_effect=custom_get_side_effect(),
            ):
                response = client.get("/auth/github/callback")

        assert response.status_code == 200

        # Verify still only one OAuth account
        oauth_count = (
            db_session.query(models.OAuthAccount)
            .filter(
                models.OAuthAccount.user_id == user.id,
                models.OAuthAccount.provider == "github",
            )
            .count()
        )
        assert oauth_count == 1


