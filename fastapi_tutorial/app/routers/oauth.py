from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app import schemas
from app.services.oauth_service import OAuthUserService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["OAuth"])

oauth = OAuth()

# GitHub OAuth
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

# Google OAuth
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    api_base_url="https://www.googleapis.com/",
    client_kwargs={
        "scope": "openid email profile",
        "prompt": "select_account",  # Forces account selection
    },
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)


@router.get("/github")
async def github_login(request: Request):
    redirect_uri = request.url_for("github_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)


@router.get("/github/callback", name="github_callback", response_model=schemas.Token)
async def github_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.github.authorize_access_token(request)

    # Fetch profile
    resp = await oauth.github.get("user", token=token)
    github_user = resp.json()

    # Fetch verified primary email (may be private and absent from profile)
    resp_emails = await oauth.github.get("user/emails", token=token)
    emails = resp_emails.json()
    primary_email = next(
        (e["email"] for e in emails if e.get("primary") and e.get("verified")),
        None,
    )

    if not primary_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No verified primary email found on GitHub account",
        )

    provider_id = str(github_user["id"])
    base_username = github_user.get("login", f"github_{provider_id}")

    # Delegate business logic to service
    oauth_service = OAuthUserService(db)
    user = oauth_service.get_or_create_user(
        provider="github",
        provider_user_id=provider_id,
        email=primary_email,
        base_username=base_username,
    )

    # Generate tokens
    auth_service = AuthService(db)
    return auth_service.create_tokens(user)


@router.get("/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", name="google_callback", response_model=schemas.Token)
async def google_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)

    # Google returns user info directly in the token response (id_token)
    # but we can also fetch it from the userinfo endpoint for consistency
    resp = await oauth.google.get("oauth2/v2/userinfo", token=token)
    google_user = resp.json()

    email = google_user.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No email found in Google account",
        )

    # Check if email is verified
    if not google_user.get("verified_email", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google email is not verified",
        )

    provider_id = str(google_user["id"])
    base_username = (
        google_user.get("name", email.split("@")[0]).replace(" ", "").lower()
    )

    # Delegate business logic to service
    oauth_service = OAuthUserService(db)
    user = oauth_service.get_or_create_user(
        provider="google",
        provider_user_id=provider_id,
        email=email,
        base_username=base_username,
    )

    # Generate tokens
    auth_service = AuthService(db)
    return auth_service.create_tokens(user)