# Start the server from PowerShell:
# py -m uvicorn main:app --reload

from fastapi import FastAPI, status, HTTPException

from database import create_tables

from schemas import CelestialObjectCreate

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

