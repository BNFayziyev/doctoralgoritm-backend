import sqlite3

def get_db_connection():
    conn = sqlite3.connect("materials.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            categories TEXT,
            file_url TEXT NOT NULL,
            preview_url TEXT
        )
    """)
    conn.commit()
    conn.close()

