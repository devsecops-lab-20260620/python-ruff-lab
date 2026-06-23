from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda name: "".join(
            [name.split("_")[0], *[part.capitalize() for part in name.split("_")[1:]]]
        ),
        populate_by_name=True,
        from_attributes=True,
    )


class ApiErrorDetail(CamelModel):
    field: str
    message: str


class ApiErrorBody(CamelModel):
    code: str
    message: str
    details: list[ApiErrorDetail] | None = None


class ApiErrorResponse(CamelModel):
    error: ApiErrorBody


class RoleType(StrEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class BookStatusType(StrEnum):
    UNREAD = "unread"
    READING = "reading"
    READ = "read"


class UserRead(CamelModel):
    id: str
    name: str
    email: EmailStr
    role: RoleType
    created_at: datetime
    updated_at: datetime


class UserCreate(CamelModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: RoleType = RoleType.USER


class UserUpdate(CamelModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: RoleType | None = None


class PagedUsers(CamelModel):
    items: list[UserRead]
    total: int
    page: int
    limit: int


class BookRead(CamelModel):
    id: str
    title: str
    author: str
    isbn: str
    publisher: str | None = None
    published_year: int | None = None
    status: BookStatusType
    owner_user_id: str | None = None
    note: str | None = None
    created_at: datetime
    updated_at: datetime


class BookCreate(CamelModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=120)
    isbn: str = Field(min_length=10, max_length=32)
    publisher: str | None = Field(default=None, max_length=255)
    published_year: int | None = Field(default=None, ge=1000, le=3000)
    status: BookStatusType = BookStatusType.UNREAD
    owner_user_id: str | None = None
    note: str | None = None


class BookUpdate(CamelModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    author: str | None = Field(default=None, min_length=1, max_length=120)
    isbn: str | None = Field(default=None, min_length=10, max_length=32)
    publisher: str | None = Field(default=None, max_length=255)
    published_year: int | None = Field(default=None, ge=1000, le=3000)
    status: BookStatusType | None = None
    owner_user_id: str | None = None
    note: str | None = None


class PagedBooks(CamelModel):
    items: list[BookRead]
    total: int
    page: int
    limit: int


class LoginRequest(CamelModel):
    email: EmailStr
    password: str = Field(min_length=1)


class LoginResponse(CamelModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: UserRead


class MessageResponse(CamelModel):
    message: str


class HealthResponse(CamelModel):
    status: str
    service: str
    version: str


def error_payload(
    code: str,
    message: str,
    details: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    body = {"code": code, "message": message}
    if details:
        body["details"] = details
    return {"error": body}


