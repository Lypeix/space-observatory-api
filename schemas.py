from pydantic import BaseModel, ConfigDict, Field

class StrippedModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

class CelestialObjectCreate(StrippedModel):
    name: str = Field(min_length=1, max_length=100)
    object_type: str = Field(min_length=1, max_length=100)
    distance_light_years: float = Field(ge=0)
    potentially_habitable: bool
    description: str = Field(min_length=1, max_length=500)

class CelestialObjectUpdate(StrippedModel):
    name: str = Field(min_length=1, max_length=100)
    object_type: str = Field(min_length=1, max_length=100)
    distance_light_years: float = Field(ge=0)
    potentially_habitable: bool
    description: str = Field(min_length=1, max_length=500)

class ObservationCreate(StrippedModel):
    observer: str = Field(min_length=1, max_length=100)
    details: str = Field(min_length=1, max_length=1000)