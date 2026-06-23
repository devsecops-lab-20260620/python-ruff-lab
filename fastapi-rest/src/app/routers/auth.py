from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user, revoke_token, verify_password
from app.config import settings
from app.database import get_db
from app.errors import ApiError
from app.models import User
from app.schemas import LoginRequest, LoginResponse, MessageResponse

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
logout_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.password_hash):
        raise ApiError(401, "UNAUTHORIZED", "認証に失敗しました")

    token = create_access_token(user.id)
    return LoginResponse(
        access_token=token,
        token_type="Bearer",
        expires_in=settings.access_token_expire_seconds,
        user=user,
    )


@router.post("/logout", response_model=MessageResponse)
def logout(_: User = Depends(get_current_user), token: str = Depends(logout_oauth2)) -> MessageResponse:
    revoke_token(token)
    return MessageResponse(message="Logged out")

