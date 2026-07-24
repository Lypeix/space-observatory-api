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
- Added CelestialObjectUpdate Pydantic schema
- Added insert_celestial_object to database.py
- Added POST objects to main.py that interacts with insert_celestial_object
- Ran the app and experimented with SwaggerUI

## DAY 2 - 21.07.2026
### Session 1 (~90mins)
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

### Session 2 (~75mins)
- Reconstructed main.py n schemas.py
- Theorised about how GET, POST, PUT, DELETE requests might look in a proper app like Steam
- Implemented comment explanation for model_dump
- Added get_celestial_objects() into database
- Wired GET endpoint to get_celestial_objects() in the database layer
- Created row_to_celestial_object() helper in the database so that booleans are returned as true/false instead of SQLite's 0/1
- Replaced repeated row conversion code in the database functions with the helper
- Implemented get_celestial_object_by_id() to view only one object chosen by its id
- Wired GET /objects/{object_id} to the db lookup func
- Added 404 response for ids that dont exist
- Tested the new functions with SwaggerUI

## DAY 3 - 22.07.2026
### Session 1 (~35mins)
- Reconstructed yesterday's db functions from memory in sql_reconstruction
- Implemented update_celestial_object() in the database layer
- Wired PUT endpoint to update_celestial_object()
- Tested the new update with SwaggerUI

### Session 2 (~15mins)
- Added delete_celestial_object() in the database layer
- Hooked up delete_celestial_object() through DELETE endpoint
- Tested the new function with SwaggerUI
- Completed the database-backed CRUD section

## DAY 4 - 23.07.2026
### Session 1 (~80mins)
- Extended get_celestial_objects() with:
    - optional case-insensitive name searching
    - object type filter
    - potentially habitable filter
    - limit
    - offset
- Added validated query parameters to GET /objects 
- Tested name searching, filtering and pagination with SwaggerUI
- Added few comments and a reference

## DAY 5 - 24.07.2026
### Session 1 (~25mins)
- Enabled SQLite Foreign Keys
- Created observation table
- Linked observations to celestial_objects through a romantic relationship
- Added cascading deletion ensuring observations wont outlast their partners