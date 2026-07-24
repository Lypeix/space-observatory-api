import sqlite3

from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "space_observatory.db" 


def connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row # changes fetched db rows from tuples into rows that can be accessed through column names n converted into dicts
    connection.execute("PRAGMA foreign_keys = on")

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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        object_id INTEGER NOT NULL,

        observer TEXT NOT NULL,

        details TEXT NOT NULL,

        observed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (object_id)
            REFERENCES celestial_objects(id)
            ON DELETE CASCADE 
    ) 
""")            # FOREIGN KEY - Sets up the stage for different table to be referenced (relationship)
                # References - Assigns observations.object_id to celestial_object.id (NOT observation id)
                # ON DELETE CASCADE - Deletes all observations alligned with the deleted object

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

def row_to_observation(row):
    if row is None:
        return None

    return dict(row)

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

def get_celestial_objects(
    name: str | None = None,
    object_type: str | None = None,
    potentially_habitable: bool | None = None,
    limit: int = 50,
    offset: int = 0 # skips rows regardless of ids
):

    connection = connect()
    cursor = connection.cursor()

    query = """
        SELECT
            id,
            name,
            object_type,
            distance_light_years,
            potentially_habitable,
            description,
            created_at
        FROM celestial_objects
    """

    conditions = []
    parameters = []

    if name is not None:
        conditions.append(
            "LOWER(name) LIKE LOWER(?)"
        )
        parameters.append(f"%{name}%")

    if object_type is not None:
        conditions.append(
            "LOWER(object_type) = LOWER(?)"
        )
        parameters.append(object_type)

    if potentially_habitable is not None:
        conditions.append(
            "potentially_habitable = ?"
        )
        parameters.append(int(potentially_habitable))

    if conditions:
        query += " WHERE " + " AND ".join(conditions) # WHERE keeps the rows matching filters
                                                      # AND.join(conditions) is for more than 1 filter to be included

    query += """
        ORDER BY id ASC
        LIMIT ?
        OFFSET ? 
    """

    parameters.extend([limit, offset])

    cursor.execute(query, parameters)

    rows = cursor.fetchall()
    connection.close()

    return [row_to_celestial_object(row) for row in rows]

# IF NO FILTERS APPLIED, THERE WILL BE NO "WHERE" OR "AND" SESSION
# STRUCTURE EXAMPLE:
#    query = """
#        SELECT ...
#        FROM celestial_objects
#        WHERE LOWER(name) LIKE LOWER(?) (LOWER always converts texts to lower case so its case-insensitive)
#        AND LOWER(object_type) = LOWER(?) 
#        ORDER BY id ASC (ascending order)
#        LIMIT ?
#        OFFSET ?
#    """
#    parameters match each ? from left to right
#    parameters = ["%TON 618%", "Black Hole", 10, 0]
#                     name          type   limit, offset


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


def delete_celestial_object(object_id: int):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM celestial_objects
        WHERE id = ?
    """, (object_id,))

    deleted_object = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted_object


def insert_observation(
    object_id: int,
    observation_data: dict
    ):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 1
    FROM celestial_objects
    WHERE id = ?
""", (object_id,))

    object_exists = cursor.fetchone()

    if not object_exists: 
        connection.close()
        return None

    cursor.execute("""
    INSERT INTO observations (
        object_id,
        observer,
        details
    )
    VALUES (?, ?, ?)
""", (
    object_id,
    observation_data["observer"],
    observation_data["details"]
    )
)

    observation_id = cursor.lastrowid
    connection.commit()

    cursor.execute("""
    SELECT
        id,
        object_id,
        observer,
        details,
        observed_at
    FROM observations
    WHERE id = ?
""", (observation_id,))

    created_row = cursor.fetchone()
    connection.close()

    return row_to_observation(created_row)

def get_observations(object_id: int):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 1
    FROM celestial_objects
    WHERE id = ?
""", (object_id,))

    object_exists = cursor.fetchone()

    if not object_exists:
        connection.close()
        return None

    cursor.execute("""
    SELECT 
        id,
        object_id,
        observer,
        details,
        observed_at
    FROM observations
    WHERE object_id = ?
    ORDER BY id ASC
""", (object_id,))

    rows = cursor.fetchall()
    connection.close()

    return [row_to_observation(row) for row in rows]
