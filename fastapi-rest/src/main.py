from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.errors import register_exception_handlers
from app.models import Role, User
from app.routers.auth import router as auth_router
from app.routers.books import router as books_router
from app.routers.health import router as health_router
from app.routers.users import router as users_router


def initialize_data(db: Session) -> None:
    admin_email = "admin@example.com"
    exists = db.scalar(select(User).where(User.email == admin_email))
    if exists:
        return

    admin = User(
        name="System Admin",
        email=admin_email,
        role=Role.ADMIN,
        password_hash=hash_password("password123"),
    )
    db.add(admin)
    db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        initialize_data(db)
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
register_exception_handlers(app)
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(users_router)

