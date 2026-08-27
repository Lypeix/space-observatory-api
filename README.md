# Space Observatory API

Database-backed REST API built with FastAPI and SQLite for cataloguing celestial objects and recording observations. 

See: [DEVLOG.md](./DEVLOG.md)

## How to run:

### Install dependencies:

1. Open PowerShell in the project directory
2. Type `py -m pip install -r requirements.txt`

### Start the Server:
1. Type `py -m uvicorn main:app --reload`
2. Open API documentation `http://127.0.0.1:8000/docs`

### Usage examples:

1. Click `POST /objects` to create a celestial body
    Example value:
        {
        "name": "string",
        "object_type": "string",
        "distance_light_years": 0,
        "potentially_habitable": true,
        "description": "string"
        }

2. Click `POST /objects/{object_id}/observations` to add an observation to your celestial body
    Example value:
        {
        "observer": "string",
        "details": "string"
        }

3. Click `GET /objects` to list out all objects

4. View specific object with `GET /objects/{object_id}` or `GET /objects/{object_id}/observations`

5. Click `DELETE /objects/{object_id}` to delete the object and all of its observations

6. Click `PUT /objects/{object_id}` to update a specific celestial body

### Run tests

```powershell
py -m pytest
```

### Features
```markdown
- CRUD operations for celestial objects
- Nested observations connected through foreign keys
- Name searching, filtering, and pagination
- Pydantic request validation
- Consistent `404 Not Found` responses
- Cascading deletion of related observations
- Automated API tests
```

### Tech Stack

- Python
- FastAPI
- SQLite
- Pydantic
- pytest

### Project Structure

```text
space-observatory-api/
|-- database.py
|-- DEVLOG.md
|-- main.py
|-- README.md
|-- requirements.txt
|-- schemas.py
`-- tests/
    `-- test_api.py
```

Developed with assistance from Codex 5.6 SOL