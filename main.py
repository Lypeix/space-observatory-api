# Start the server from PowerShell:
# py -m uvicorn main:app --reload

from fastapi import FastAPI, status, HTTPException

from pydantic import BaseModel, Field

from database import create_tables

app = FastAPI(
    title="Space Observatory API",
    description="Cool API project for cataloguing celestial objects and observations"
)

create_tables()

class CelestialObjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    object_type: str = Field(min_length=1, max_length=100)
    distance_light_years: float = Field(ge=0)
    potentially_habitable: bool
    description: str = Field(min_length=1, max_length=500)

@app.get("/")
def root():
    return {
        "message": "The Space Observatory API is fully operational! "
    }

