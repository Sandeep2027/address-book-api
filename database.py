import sqlite3

from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        street TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        latitude REAL,
        longitude REAL
    )
    ''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON addresses (name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_lat ON addresses (latitude)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_lon ON addresses (longitude)")
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()