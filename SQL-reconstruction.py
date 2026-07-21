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