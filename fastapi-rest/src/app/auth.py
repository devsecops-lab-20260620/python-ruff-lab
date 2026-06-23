from datetime import UTC, datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.errors import ApiError
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
_revoked_tokens: set[str] = set()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(seconds=settings.access_token_expire_seconds)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise ApiError(401, "UNAUTHORIZED", "トークンが不正です")
        return str(user_id)
    except JWTError as exc:
        raise ApiError(401, "UNAUTHORIZED", "トークンが不正、または期限切れです") from exc


def revoke_token(token: str) -> None:
    _revoked_tokens.add(token)


def is_token_revoked(token: str) -> bool:
    return token in _revoked_tokens


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    if is_token_revoked(token):
        raise ApiError(401, "UNAUTHORIZED", "トークンが不正、または期限切れです")

    user_id = decode_access_token(token)
    user: User | None = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ApiError(401, "UNAUTHORIZED", "認証に失敗しました")
    return user

