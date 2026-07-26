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

def create_test_object(client): # creates object for tests that need it
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

def test_get_objects(client):
    created_object = create_test_object(client)

    response = client.get("/objects")

    assert response.status_code == 200
    assert response.json() == [created_object]

def test_update_objects(client):
    created_object = create_test_object(client)
    object_id = created_object["id"]


    response = client.put(f"/objects/{object_id}", json=UPDATED_OBJECT_DATA)

    assert response.status_code == 200

    updated_object = response.json()

    assert updated_object["id"] == object_id
    assert updated_object["name"] == "Kepler-186f Updated"
    assert updated_object["potentially_habitable"] is False

def test_delete_objects(client):
    created_object = create_test_object(client)
    object_id = created_object["id"]

    delete_response = client.delete(f"/objects/{object_id}")

    assert delete_response.status_code == 200

    get_response = client.get(f"/objects/{object_id}")

    assert get_response.status_code == 404

def test_missing_object_returns_404(client): # checks HTTPExceptions
    assert client.get("/objects/999").status_code == 404

    assert client.put("/objects/999", json=UPDATED_OBJECT_DATA).status_code == 404

    assert client.delete("/objects/999").status_code == 404

    assert client.post("/objects/999/observations", json=OBSERVATION_DATA).status_code == 404 # proves observation cant be attached to a non-existent object

def test_invalid_object_returns_422(client):
    invalid_object = OBJECT_DATA.copy()
    invalid_object["distance_light_years"] = -10

    response = client.post("/objects", json=invalid_object)

    assert response.status_code == 422

def test_whitespace_name_returns_422(client):
    invalid_object = OBJECT_DATA.copy()
    invalid_object["name"] = " "

    response = client.post("/objects", json=invalid_object)

    assert response.status_code == 422

def test_create_and_get_observations(client):
    created_object = create_test_object(client)
    object_id = created_object["id"]

    create_response = client.post(f"/objects/{object_id}/observations", json=OBSERVATION_DATA)

    assert create_response.status_code == 201

    created_observation = create_response.json()

    assert created_observation["object_id"] == object_id
    assert created_observation["observer"] == "Lypeix"

    get_response = client.get(f"/objects/{object_id}/observations")

    assert get_response.status_code == 200

    assert get_response.json() == [created_observation]