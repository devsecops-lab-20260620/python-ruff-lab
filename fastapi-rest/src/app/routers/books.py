from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional

from app.auth import get_current_user
from app.database import get_db
from app.errors import ApiError
from app.models import Book, BookStatus, User
from app.schemas import BookCreate, BookRead, BookStatusType, BookUpdate, PagedBooks

router = APIRouter(prefix="/api/v1/books", tags=["books"])


def _status_to_model(status_param: Optional[BookStatusType]) -> Optional[BookStatus]:
    if status_param is None:
        return None
    return BookStatus(status_param.value)


@router.get("", response_model=PagedBooks)
def list_books(
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    keyword: Optional[str] = None,
    owner_user_id: Optional[str] = Query(default=None, alias="ownerUserId"),
    status_param: Optional[BookStatusType] = Query(default=None, alias="status"),
) -> PagedBooks:
    query = select(Book)
    count_query = select(func.count(Book.id))

    filters = []
    if keyword:
        pattern = f"%{keyword}%"
        filters.append(or_(Book.title.ilike(pattern), Book.author.ilike(pattern), Book.isbn.ilike(pattern)))
    if owner_user_id:
        filters.append(Book.owner_user_id == owner_user_id)
    status_model = _status_to_model(status_param)
    if status_model:
        filters.append(Book.status == status_model)

    if filters:
        query = query.where(*filters)
        count_query = count_query.where(*filters)

    total = db.scalar(count_query) or 0
    items = db.scalars(query.offset((page - 1) * limit).limit(limit)).all()
    return PagedBooks(items=items, total=total, page=page, limit=limit)


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    payload: BookCreate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BookRead:
    if payload.owner_user_id and not db.get(User, payload.owner_user_id):
        raise ApiError(400, "VALIDATION_ERROR", "ownerUserId が存在しません")

    book = Book(
        title=payload.title,
        author=payload.author,
        isbn=payload.isbn,
        publisher=payload.publisher,
        published_year=payload.published_year,
        status=BookStatus(payload.status.value),
        owner_user_id=payload.owner_user_id,
        note=payload.note,
    )
    db.add(book)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ApiError(409, "CONFLICT", "isbn が重複しています") from exc

    db.refresh(book)
    return book


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: str, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> BookRead:
    book = db.get(Book, book_id)
    if not book:
        raise ApiError(404, "NOT_FOUND", "書籍が見つかりません")
    return book


@router.patch("/{book_id}", response_model=BookRead)
def update_book(
    book_id: str,
    payload: BookUpdate,
    _: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> BookRead:
    book = db.get(Book, book_id)
    if not book:
        raise ApiError(404, "NOT_FOUND", "書籍が見つかりません")

    if payload.owner_user_id is not None and payload.owner_user_id != "":
        if not db.get(User, payload.owner_user_id):
            raise ApiError(400, "VALIDATION_ERROR", "ownerUserId が存在しません")

    updates = payload.model_dump(exclude_unset=True)
    for key, value in updates.items():
        if key == "status" and value is not None:
            setattr(book, key, BookStatus(value))
        else:
            setattr(book, key, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise ApiError(409, "CONFLICT", "isbn が重複しています") from exc

    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str, _: User = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    book = db.get(Book, book_id)
    if not book:
        raise ApiError(404, "NOT_FOUND", "書籍が見つかりません")

    db.delete(book)
    db.commit()


