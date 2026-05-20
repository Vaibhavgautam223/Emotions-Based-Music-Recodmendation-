import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "moodtunes.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT    UNIQUE NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            mood       TEXT    NOT NULL,
            songs_json TEXT    NOT NULL,
            played_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
    )
    conn.commit()
    conn.close()


def create_user(username, email, password_hash):
    conn = get_conn()
    conn.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        (username, email, password_hash),
    )
    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_email(email):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return dict(row) if row else None


def save_session(user_id, mood, songs):
    conn = get_conn()
    conn.execute(
        "INSERT INTO sessions (user_id, mood, songs_json) VALUES (?, ?, ?)",
        (user_id, mood, json.dumps(songs)),
    )
    conn.commit()
    conn.close()


def get_history(user_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT mood, songs_json, played_at FROM sessions WHERE user_id = ? ORDER BY played_at DESC LIMIT 20",
        (user_id,),
    ).fetchall()
    conn.close()
    return [
        {
            "mood": row["mood"],
            "songs": json.loads(row["songs_json"]),
            "played_at": row["played_at"],
        }
        for row in rows
    ]
