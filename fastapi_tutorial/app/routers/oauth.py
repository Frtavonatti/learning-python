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
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
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

    # Look up existing OAuth user
    user = db.query(models.User).filter(
        models.User.oauth_providers == "github",
        models.User.oauth_provider_id == provider_id,
    ).first()

    if not user:
        # Check if the email is already registered (local account)
        user = db.query(models.User).filter(models.User.email == primary_email).first()
        if user:
            # Link OAuth to existing account
            user.oauth_providers = "github"
            user.oauth_provider_id = provider_id
        else:
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
                oauth_providers="github",
                oauth_provider_id=provider_id,
            )
            db.add(user)

        db.commit()
        db.refresh(user)

    access_token = create_access_token(subject=str(user.id), roles=user.roles)
    refresh_token = create_refresh_token(subject=str(user.id))

    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )