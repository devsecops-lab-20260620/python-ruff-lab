from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class BookStatus(StrEnum):
    UNREAD = "unread"
    READING = "reading"
    READ = "read"


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False, default=Role.USER)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )


class Book(Base):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(120), nullable=False)
    isbn: Mapped[str] = mapped_column(String(32), nullable=False, unique=True, index=True)
    publisher: Mapped[str | None] = mapped_column(String(255), nullable=True)
    published_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[BookStatus] = mapped_column(Enum(BookStatus), nullable=False, default=BookStatus.UNREAD)
    owner_user_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True, index=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

