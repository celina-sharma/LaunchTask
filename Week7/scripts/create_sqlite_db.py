import sqlite3
import csv
from pathlib import Path

DB_PATH = Path("src/data/sql/music.db")
DATA_DIR = Path("src/data/sql")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS sales;

CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE albums (
    album_id INTEGER PRIMARY KEY,
    artist_id INTEGER,
    title TEXT,
    release_year INTEGER,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    album_id INTEGER,
    year INTEGER,
    amount REAL,
    FOREIGN KEY (album_id) REFERENCES albums(album_id)
);
""")

def load_csv(table, columns):
    with open(DATA_DIR / f"{table}.csv", newline="") as f:
        reader = csv.DictReader(f)
        rows = [tuple(row[c] for c in columns) for row in reader]
        placeholders = ",".join("?" * len(columns))
        cur.executemany(
            f"INSERT INTO {table} VALUES ({placeholders})",
            rows
        )

load_csv("artists", ["artist_id", "name"])
load_csv("albums", ["album_id", "artist_id", "title", "release_year"])
load_csv("sales", ["sale_id", "album_id", "year", "amount"])

conn.commit()
conn.close()

print("SQLite database")
