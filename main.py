# Start the server from PowerShell:
# py -m uvicorn main:app --reload

from fastapi import FastAPI, status, HTTPException

from database import create_tables, insert_celestial_object

from schemas import CelestialObjectCreate, CelestialObjectUpdate

app = FastAPI(
    title="Space Observatory API",
    description="Cool API project for cataloguing celestial objects and observations"
)

create_tables()

@app.get("/")
def root():
    return {
        "message": "The Space Observatory API is fully operational! "
    }

@app.post("/objects", status_code=status.HTTP_201_CREATED)
def create_object(object_data: CelestialObjectCreate): 
    return insert_celestial_object(object_data.model_dump()) # model_dump converts pydantic into normal python dict so that SQLite can understand the ongoing lingo
    