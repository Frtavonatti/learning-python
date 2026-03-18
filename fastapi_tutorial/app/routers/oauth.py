from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.auth.jwt_handler import create_access_token, create_refresh_token
from app import models, schemas

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

    # Look up existing OAuth account
    oauth_account = db.query(models.OAuthAccount).filter(
        models.OAuthAccount.provider == "github",
        models.OAuthAccount.provider_user_id == provider_id,
    ).first()

    if oauth_account:
        # OAuth account exists, return tokens for that user
        user = oauth_account.user
    else:
        # Check if the email is already registered (local account or different OAuth)
        user = db.query(models.User).filter(models.User.email == primary_email).first()
        
        if not user:
            # Create a new user from GitHub profile
            base_username = github_user.get("login", f"github_{provider_id}")
            username = base_username
            suffix = 1
            while db.query(models.User).filter(models.User.username == username).first():
                username = f"{base_username}_{suffix}"
                suffix += 1

            user = models.User(
                email=primary_email,
                username=username,
                hashed_password=None,
                roles=[],
            )
            db.add(user)
            db.flush()  # Get user.id before creating oauth_account

        # Link OAuth provider to user (works for both new and existing users)
        oauth_account = models.OAuthAccount(
            user_id=user.id,
            provider="github",
            provider_user_id=provider_id,
        )
        db.add(oauth_account)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(subject=str(user.id), roles=user.roles)
    refresh_token = create_refresh_token(subject=str(user.id))

    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


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

    # Look up existing OAuth account
    oauth_account = db.query(models.OAuthAccount).filter(
        models.OAuthAccount.provider == "google",
        models.OAuthAccount.provider_user_id == provider_id,
    ).first()

    if oauth_account:
        # OAuth account exists, return tokens for that user
        user = oauth_account.user
    else:
        # Check if the email is already registered (local account or different OAuth)
        user = db.query(models.User).filter(models.User.email == email).first()
        
        if not user:
            # Create a new user from Google profile
            # Use the part before @ as base username
            base_username = google_user.get("name", email.split("@")[0]).replace(" ", "").lower()
            username = base_username
            suffix = 1
            while db.query(models.User).filter(models.User.username == username).first():
                username = f"{base_username}_{suffix}"
                suffix += 1

            user = models.User(
                email=email,
                username=username,
                hashed_password=None,
                roles=[],
            )
            db.add(user)
            db.flush()  # Get user.id before creating oauth_account

        # Link OAuth provider to user (works for both new and existing users)
        oauth_account = models.OAuthAccount(
            user_id=user.id,
            provider="google",
            provider_user_id=provider_id,
        )
        db.add(oauth_account)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(subject=str(user.id), roles=user.roles)
    refresh_token = create_refresh_token(subject=str(user.id))

    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )