# Start the server from PowerShell:
# py -m uvicorn main:app --reload

from fastapi import FastAPI, status, Query, HTTPException

from database import create_tables, insert_celestial_object, get_celestial_objects, get_celestial_object_by_id, update_celestial_object, delete_celestial_object

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
def list_celestial_objects(
    name: str | None = Query(
        default=None,
        min_length=1,
        max_length=100
    ),

    object_type: str | None = Query(
        default=None,
        min_length=1,
        max_length=150
    ),

    potentially_habitable: bool | None = Query(
        default=None
    ),

    limit: int = Query(
        default=50,
        ge=1, # great or equal to 1
        le=100 # lesser or equal to 100 so limit is between 1 and 100.
    ),
    offset: int = Query(
        default=0,
        ge=0
    )
):
    
    return get_celestial_objects(
        name, 
        object_type,
        potentially_habitable,
        limit,
        offset
        )


@app.get("/objects/{object_id}")
def get_object(object_id: int):
    celestial_object = get_celestial_object_by_id(object_id)

    if celestial_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Celestial object not found"
            ) 
    
    return celestial_object


@app.put("/objects/{object_id}")
def update_object(object_id: int, object_data: CelestialObjectUpdate):
    celestial_object = update_celestial_object(
        object_id,
        object_data.model_dump()
    )

    if celestial_object is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Celestial object not found"
        )

    return celestial_object


@app.delete("/objects/{object_id}")
def delete_object(object_id: int):
    deleted_object = delete_celestial_object(object_id)

    if not deleted_object:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Celestial object not found"
        )

    return {
        "message": "Object has been successfuly deleted",
        "object": object_id
    }



