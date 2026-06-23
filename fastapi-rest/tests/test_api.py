import os
import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Importing app after setting environment keeps tests isolated from local DB settings.
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///./test_fastapi_rest.db"
os.environ["JWT_SECRET"] = "test-secret"

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client


def _login(client: TestClient) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    return response.json()["accessToken"]


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_user_and_book_flow(client: TestClient) -> None:
    token = _login(client)
    headers = {"Authorization": f"Bearer {token}"}

    user_payload = {
        "name": "Taro Yamada",
        "email": "taro@example.com",
        "password": "password123",
        "role": "user",
    }
    create_user = client.post("/api/v1/users", json=user_payload, headers=headers)
    assert create_user.status_code == 201
    user_id = create_user.json()["id"]

    list_users = client.get("/api/v1/users?page=1&limit=10&keyword=taro", headers=headers)
    assert list_users.status_code == 200
    assert list_users.json()["total"] >= 1

    book_payload = {
        "title": "Domain-Driven Design",
        "author": "Eric Evans",
        "isbn": "978-4-7819-1628-6",
        "status": "unread",
        "ownerUserId": user_id,
    }
    create_book = client.post("/api/v1/books", json=book_payload, headers=headers)
    assert create_book.status_code == 201
    book_id = create_book.json()["id"]

    get_book = client.get(f"/api/v1/books/{book_id}", headers=headers)
    assert get_book.status_code == 200
    assert get_book.json()["ownerUserId"] == user_id


