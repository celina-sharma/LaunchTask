import sqlite3

DB_PATH = "src/data/sql/music.db"

def execute_sql(sql: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    conn.close()
    return [dict(zip(columns, row)) for row in rows]
