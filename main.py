# Start the server from PowerShell:
# py -m uvicorn main:app --reload

from fastapi import FastAPI, status, HTTPException

from database import create_tables, insert_celestial_object, get_celestial_objects, get_celestial_object_by_id

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


@app.get("/objects") # returns status code 200 OK by default
def list_celestial_objects():
    return get_celestial_objects()

@app.get("/objects/{object_id}")
def get_object(object_id: int):
    celestial_object = get_celestial_object_by_id(object_id)

    if celestial_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Celestial object not found"
            ) 
    
    return celestial_object