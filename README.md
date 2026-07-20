# Space Observatory API

Backend project featuring FastAPI and SQL for "observing" celestial bodies and recording the observations

## Roadmap

### Foundation

- [ ] Create multi-file project structure
- [ ] Install FastAPI, Uvicorn, and pytest
- [ ] Create FastAPI app instance
- [ ] Create SQLite connection helper
- [ ] Create `celestial_objects` table
- [ ] Enable automatic table creation during development

### Database-Backed CRUD

- [ ] Add `CelestialObjectCreate` Pydantic schema
- [ ] Add `CelestialObjectUpdate` Pydantic schema
- [ ] Add `POST /objects`
- [ ] Add `GET /objects`
- [ ] Add `GET /objects/{object_id}`
- [ ] Add `PUT /objects/{object_id}`
- [ ] Add `DELETE /objects/{object_id}`
- [ ] Replace all in-memory storage with SQLite queries
- [ ] Return `404 Not Found` for missing objects
- [ ] Add Pydantic field validation

### Querying

- [ ] Add search by object name
- [ ] Add filtering by object type
- [ ] Add filtering by potential habitability
- [ ] Add `limit` and `offset` pagination
- [ ] Add automatic creation timestamps

### Observations

- [ ] Create `observations` table
- [ ] Associate observations with celestial objects using `object_id`
- [ ] Add `POST /objects/{object_id}/observations`
- [ ] Add `GET /objects/{object_id}/observations`
- [ ] Prevent observations from being added to nonexistent objects

### Quality

- [ ] Add API tests using FastAPI `TestClient`
- [ ] Test successful CRUD operations
- [ ] Test `404` responses
- [ ] Test Pydantic validation errors
- [ ] Add setup and run instructions
- [ ] Add API usage examples
- [ ] Document known limitations

## Project Structure

``` space-observatory-api/
├── main.py          # FastAPI app and endpoints
├── database.py      # SQLite connection, tables, and queries
├── schemas.py       # Pydantic request models
├── tests/
│   └── test_api.py  # API tests
└── 
