import sqlite3

DB_PATH = "heimdal.db"

def initialize():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS builds (
        id INTEGER PRIMARY KEY,
        name TEXT,
        created_at DATETIME,
        status TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        build_id INTEGER,
        name TEXT,
        status TEXT,
        priority INTEGER
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        task_id INTEGER,
        timestamp DATETIME,
        message TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS learnings (
        id INTEGER PRIMARY KEY,
        task_name TEXT,
        failure_count INTEGER,
        average_duration INTEGER
    )''')

    conn.commit()
    conn.close()
