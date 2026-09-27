import os
from pathlib import Path


TEST_DB = Path(
    "test_pocketsmart.db"
)


os.environ["DATABASE_URL"] = (
    f"sqlite:///{TEST_DB}"
)

os.environ["SECRET_KEY"] = (
    "test-secret-key"
)


from fastapi.testclient import TestClient

from app.main import app

from app.database import (
    Base,
    engine,
)


client = TestClient(app)


def setup_module():

    Base.metadata.drop_all(
        bind=engine
    )

    Base.metadata.create_all(
        bind=engine
    )


def teardown_module():

    Base.metadata.drop_all(
        bind=engine
    )

    if TEST_DB.exists():
        TEST_DB.unlink()


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "PocketSmart AI" in response.text


def test_register_and_login():

    response = client.post(
        "/register",

        data={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },

        follow_redirects=False,
    )

    assert response.status_code == 303

    assert (
        response.headers["location"]
        == "/dashboard"
    )


    client.post(
        "/logout",
        follow_redirects=False
    )


    response = client.post(
        "/login",

        data={
            "email": "test@example.com",
            "password": "password123",
        },

        follow_redirects=False,
    )

    assert response.status_code == 303


def test_home_planner_requires_login():

    client.post(
        "/logout",
        follow_redirects=False
    )


    response = client.post(
        "/recommendations/home",

        data={
            "total_budget": "50000",
            "room_type": "Living Room",
            "room_size": "12x14",
            "preferred_style": "Modern",
            "color_preference": "Neutral",
            "number_of_items": "5",
            "additional_requirements": "",
        },
    )

    assert response.status_code == 401