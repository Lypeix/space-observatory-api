import pytest # provides

from fastapi.testclient import TestClient

import database

from main import app

OBJECT_DATA = {
    "name": "Kepler-186f",
    "object_type": "exoplanet",
    "distance_light_years": 582,
    "potentially_habitable": True,
    "description": "An Earth-sized exoplanet."
}

UPDATED_OBJECT_DATA = {
    "name": "Kepler-186f Updated",
    "object_type": "planet",
    "distance_light_years": 580,
    "potentially_habitable": False,
    "description": "Updated description."
}

OBSERVATION_DATA = {
    "observer": "Lypeix",
    "details": "It seems rounder than the last time"
}

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test_observatory.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database
    )

    with TestClient(app) as test_client:
        yield test_client

