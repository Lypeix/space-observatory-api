import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent / "training.db"
                    

def connect():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row # gives option to convert rows into dicts, then json bodies, very useful

    return connection


def create_table():
    connection = connect()
    cursor = connection.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS training_plushies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
            
        name TEXT NOT NULL,
                   
        kg REAL NOT NULL 
            CHECK (kg >= 0),
                   
        cute INTEGER NOT NULL
            CHECK (cute in (0, 1)),
                   
        description TEXT NOT NULL,
                   
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                   
        )
    """)

    connection.commit()
    connection.close()

def row_to_plushie(row):
    if row is None:
        return None

    plushie_data = dict(row)

    plushie_data["cute"] = bool(
        plushie_data["cute"]
    )

    return plushie_data


def insert_training_plushie(plushie_data: dict):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""

    INSERT INTO training_plushies (
        name,
        kg,
        cute,
        description
    )
                   
    VALUES (?, ?, ?, ?)
    """,
    (
        plushie_data["name"],
        plushie_data["kg"],
        plushie_data["cute"],
        plushie_data["description"]
    )    
)
    
    plushie_id = cursor.lastrowid
    connection.commit()

    cursor.execute("""
    SELECT *
    FROM training_plushies
    WHERE id = ?
    """,
        (plushie_id,), 
)
    row = cursor.fetchone()
    connection.close()

    return row_to_plushie(row)

def get_plushies():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT 
        id,
        name,
        kg,
        cute,
        description
    FROM training_plushies
    ORDER BY id ASC
""")

    rows = cursor.fetchall()
    connection.close()

    plushies_list = []

    for row in rows:
        plushies_list.append(
        row_to_plushie(row)
        )

    return plushies_list

def get_plushie_by_id(plushie_id: int):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        id,
        name,
        kg,
        cute,
        description
    FROM training_plushies
    WHERE id = ?
    
""",
    (plushie_id,))

    row = cursor.fetchone()
    connection.close()

    return row_to_plushie(row)