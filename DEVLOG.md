# !DEVLOG!

## DAY 1 - 20.07.2026
### Session 1 (~190mins)
- Installed Git
- Integrated Git with VSC
- Learned basic Git commands (add, commit, push, pull)
- Cloned the Github repo and connected it to the local project 
- Created learning roadmap
- Added the multi-file structure 
- Added SQLite connection in database.py 
- Defined initial table for celestial_objects 
- Added .gitignore to ignore pycache files
- Added FastAPI app instance
- .gitignore now also ignores generated SQLite database
- Added automatic db tables creation during app start-up
- Ran the FastAPI app with Uvicorn n checked "/" + "/docs" SwaggerUI client
- Added CelestialObjectCreate Pydantic schema
- Added CelestialUpdateCreate Pydantic schema
- Added insert_celestial_object to database.py
- Added POST objects to main.py that interacts with insert_celestial_object
- Ran the app and experimented with SwaggerUI

## DAY 2 - 21.07.2026
### Session 1 (~70mins)
- Reconstructed in different theme until able to reproduce from memory:
    - DATABASE_PATH
    - connect()
    - create_table()
    - insert_training_plushie(plushie_data: dict)
- Reviewed used concepts like:
    - Path
    - Row factory
    - Fetching
    - Overall SQLite structure
- Fought Git