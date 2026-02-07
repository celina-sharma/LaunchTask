import sqlite3

DB_PATH = "src/data/sql/music.db"

def load_db_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table';
    """)

    tables = cursor.fetchall()
    schema = {}

    for (table_name,) in tables:
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema[table_name] = [col[1] for col in cursor.fetchall()]

    conn.close()
    return schema
