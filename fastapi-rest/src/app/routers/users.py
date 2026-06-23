
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import get_current_user, hash_password
from app.database import get_db
from app.errors import ApiError
from app.models import Book, Role, User
from app.schemas import PagedUsers, RoleType, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/api/v1/users", tags=["users"])


def _role_to_model(role: RoleType | None) -> Role | None:
    if role is None:
        return None
    return Role(role.value)


@router.get("", response_model=PagedUsers)
def list_users(
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    keyword: str | None = None,
    role: RoleType | None = None,
) -> PagedUsers:
    query = select(User)
    count_query = select(func.count(User.id))

    filters = []
    if keyword:
        pattern = f"%{keyword}%"
        filters.append(or_(User.name.ilike(pattern), User.email.ilike(pattern)))
    role_model = _role_to_model(role)
    if role_model:
        filters.append(User.role == role_model)

    if filters:
        query = query.where(*filters)
        count_query = count_query.where(*filters)

    total = db.scalar(count_query) or 0
    items = db.scalars(query.offset((page - 1) * limit).limit(limit)).all()
    return PagedUsers(items=items, total=total, page=page, limit=limit)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserRead:
    user = User(
        name=payload.name,
        email=payload.email,
        role=Role(payload.role.value),
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ApiError(409, "CONFLICT", "email が重複しています") from exc

    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> UserRead:
    user = db.get(User, user_id)
    if not user:
        raise ApiError(404, "NOT_FOUND", "ユーザーが見つかりません")
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    payload: UserUpdate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserRead:
    user = db.get(User, user_id)
    if not user:
        raise ApiError(404, "NOT_FOUND", "ユーザーが見つかりません")

    if payload.name is not None:
        user.name = payload.name
    if payload.email is not None:
        user.email = payload.email
    if payload.password is not None:
        user.password_hash = hash_password(payload.password)
    if payload.role is not None:
        user.role = Role(payload.role.value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ApiError(409, "CONFLICT", "email が重複しています") from exc

    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    user = db.get(User, user_id)
    if not user:
        raise ApiError(404, "NOT_FOUND", "ユーザーが見つかりません")

    books = db.scalars(select(Book).where(Book.owner_user_id == user_id)).all()
    for book in books:
        book.owner_user_id = None

    db.delete(user)
    db.commit()


