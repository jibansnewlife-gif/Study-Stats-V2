import sqlite3

DB_PATH = "data/data.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            minutes INTEGER,
            subject TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_session(date, minutes, subject):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        "INSERT INTO sessions (date, minutes, subject) VALUES (?, ?, ?)",
        (date, minutes, subject)
    )

    conn.commit()
    conn.close()


def get_sessions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT date, minutes, subject FROM sessions")

    rows = c.fetchall()
    conn.close()

    return rows