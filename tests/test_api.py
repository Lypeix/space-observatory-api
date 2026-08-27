import pytest 

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

def create_test_object(client): 
    response = client.post("/objects", json=OBJECT_DATA)

    assert response.status_code == 201 

    return response.json() 

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

def test_missing_object_returns_404(client):
    assert client.get("/objects/999").status_code == 404

    assert client.put("/objects/999", json=UPDATED_OBJECT_DATA).status_code == 404

    assert client.delete("/objects/999").status_code == 404

    assert client.post("/objects/999/observations", json=OBSERVATION_DATA).status_code == 404 

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