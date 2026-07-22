import sqlite3

from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "space_observatory.db" 

def connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row # changes fetched db rows from tuples into rows that can be accessed through column names n converted into dicts

    return connection

def create_tables():
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

def row_to_celestial_object(row): # helper that makes that so potentially_habitable bool returns true/false to json instead of 0/1
    if row is None:
        return None
    
    object_data = dict(row)

    object_data["potentially_habitable"] = bool(
        object_data["potentially_habitable"]
    )

    return object_data

def insert_celestial_object(object_data: dict):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO celestial_objects (
            name,           
            object_type,
            distance_light_years,
            potentially_habitable,
            description
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            object_data["name"],
            object_data["object_type"],
            object_data["distance_light_years"],
            object_data["potentially_habitable"],
            object_data["description"],
        ),
    )

    object_id = cursor.lastrowid
    connection.commit()

    cursor.execute("""
        SELECT *
        FROM celestial_objects
        WHERE id = ?
    """,
        (object_id,),
    )

    created_row = cursor.fetchone()
    connection.close()

    return row_to_celestial_object(created_row)

def get_celestial_objects():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
        id,
        name,           
        object_type,
        distance_light_years,
        potentially_habitable,
        description,
        created_at
    FROM celestial_objects
    ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    connection.close()

    celestial_objects = []

    for row in rows:
        celestial_objects.append(
        row_to_celestial_object(row)
        )

    return celestial_objects 

def get_celestial_object_by_id(object_id: int):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        id,
        name,           
        object_type,
        distance_light_years,
        potentially_habitable,
        description,
        created_at
    FROM celestial_objects
    WHERE id = ?
    """, 
        (object_id,))
    
    row = cursor.fetchone()
    connection.close()

    return row_to_celestial_object(row)

def update_celestial_object(object_id: int, object_data: dict):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE celestial_objects
        SET
            name = ?,
            object_type = ?,
            distance_light_years = ?,
            potentially_habitable = ?,
            description = ?
        WHERE id = ?
    """,
        (
        object_data["name"],
        object_data["object_type"],
        object_data["distance_light_years"],
        object_data["potentially_habitable"],
        object_data["description"],
        object_id
    )
    )

    if cursor.rowcount == 0:
        connection.close()
        return None

    connection.commit()

    cursor.execute("""
        SELECT
            id,
            name,
            object_type,
            distance_light_years,
            potentially_habitable,
            description,
            created_at
        FROM celestial_objects
        WHERE id = ?
""", (object_id,))

    updated_row = cursor.fetchone()
    connection.close()

    return row_to_celestial_object(updated_row)