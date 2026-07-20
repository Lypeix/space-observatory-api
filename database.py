import sqlite3

from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "space_observatory.db" 

def connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row # changes fetched db rows from tuples into rows that can be accessed through column names n converted into dicts

    return connection

def create_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS celestial_objects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        name TEXT NOT NULL,
        
        object_type TEXT NOT NULL,
        
        distance_light_years REAL NOT NULL
                CHECK (distance_light_years >= 0),
        
        potentially_habitable INTEGER NOT NULL 
                CHECK (potentially_habitable IN (0, 1)),
        
        description TEXT NOT NULL,
        
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    connection.commit()
    connection.close()

