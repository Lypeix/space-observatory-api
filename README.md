# Space Observatory API

Database-backed REST API built with FastAPI and SQL for observing celestial bodies and recording observations. 

Developed with assistance from Codex 5.6 SOL

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

2. Click `POST /observations` to add an observation to your celestial body
    Example value:
        {
        "observer": "string",
        "details": "string"
        }

3. Click `GET /objects` to list out all objects

4. You can also view a specific object or observation by clicking `GET /objects/{object_id}` or `GET /objects/{object_id}/observations`

5. Click `DELETE /objects/{object_id}` to delete the object and all of its observations

6. Click `PUT /objects/{object_id}` to update a specific celestial body


## Project Structure

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