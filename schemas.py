from pydantic import BaseModel, Field

class CelestialObjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    object_type: str = Field(min_length=1, max_length=100)
    distance_light_years: float = Field(ge=0)
    potentially_habitable: bool
    description: str = Field(min_length=1, max_length=500)

class CelestialObjectUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    object_type: str = Field(min_length=1, max_length=100)
    distance_light_years: float = Field(ge=0)
    potentially_habitable: bool
    description: str = Field(min_length=1, max_length=500)

    