## Roadmap

### Foundation

- [x] Install and configure Git
- [x] Learn and implement Git basics
- [x] Add .gitignore to ignore pycache
- [x] Create multi-file project structure
- [x] Create FastAPI app instance
- [x] Create SQLite connection helper
- [x] Create `celestial_objects` table
- [x] Enable automatic table creation during development

### Database-Backed CRUD

- [x] Add `CelestialObjectCreate` Pydantic schema
- [x] Add `CelestialObjectUpdate` Pydantic schema
- [x] Add Pydantic field validation
- [x] Add `POST /objects`
- [x] Add `GET /objects`
- [x] Add `GET /objects/{object_id}`
- [x] Add `PUT /objects/{object_id}`
- [x] Add `DELETE /objects/{object_id}`
- [x] Return `404 Not Found` for missing objects


### Querying

- [x] Add search by object name
- [x] Add filtering by object type
- [x] Add filtering by potential habitability
- [x] Add `limit` and `offset` pagination
- [x] Add automatic creation timestamps

### Observations

- [x] Create `observations` table
- [x] Associate observations with celestial objects using `object_id`
- [x] Add `POST /objects/{object_id}/observations`
- [x] Add `GET /objects/{object_id}/observations`
- [x] Prevent observations from being added to nonexistent objects

### Quality

- [x] Add API tests using FastAPI `TestClient`
- [x] Test successful CRUD operations
- [x] Test `404` responses
- [x] Test Pydantic validation errors