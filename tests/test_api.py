import pytest # testing framework that reads functions starting with test_ eg. test_create_object
              # provides fixtures like tmp_path n monkeypatch

from fastapi.testclient import TestClient # lets python pretend to be a client sending requests to the API without needing to launch Uvicorn

import database

from main import app

OBJECT_DATA = { # reusable og request body
    "name": "Kepler-186f",
    "object_type": "exoplanet",
    "distance_light_years": 582,
    "potentially_habitable": True,
    "description": "An Earth-sized exoplanet."
}

UPDATED_OBJECT_DATA = { # updated request body during tests
    "name": "Kepler-186f Updated",
    "object_type": "planet",
    "distance_light_years": 580,
    "potentially_habitable": False,
    "description": "Updated description."
}

OBSERVATION_DATA = { # tests observations
    "observer": "Lypeix",
    "details": "It seems rounder than the last time"
}

@pytest.fixture # turns the function into reusable test setup
def client(tmp_path, monkeypatch):
    test_database = tmp_path / "test_observatory.db" # creates path for the temp db, so that tests dont touch the actual file like space_observatory.db

    monkeypatch.setattr( # redirects the database module to the temporary test file
        database,
        "DATABASE_PATH",
        test_database
    )

    with TestClient(app) as test_client: # creates client connected to the app and runs its lifespan
        yield test_client # passes client into the test

def create_test_object(client):
    response = client.post("/objects", json=OBJECT_DATA)

    assert response.status_code == 201 # fails if API doesnt return status code 201 Created

    return response.json() # passes the created object so that the other tests can reuse it

def test_create_object(client):
    response = client.post("/objects", json=OBJECT_DATA)

    assert response.status_code == 201

    created_object = response.json()

    assert created_object["id"] == 1
    assert created_object["name"] == "Kepler-186f"
    assert created_object["potentially_habitable"] is True 
    assert "created_at" in created_object