# database.py
import sqlite3

DB_NAME = "bot.db"

def init_db():
    """SQLite database ko initialize karta hai aur user thumbnails table banata hai."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_thumbnails (
        user_id INTEGER PRIMARY KEY,
        thumbnail_path TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_thumbnail(user_id, thumbnail_path):
    """User ke thumbnail path ko database mein store (ya update) karta hai."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("REPLACE INTO user_thumbnails (user_id, thumbnail_path) VALUES (?, ?)",
              (user_id, thumbnail_path))
    conn.commit()
    conn.close()

def get_thumbnail(user_id):
    """Database se user ka stored thumbnail path return karta hai."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT thumbnail_path FROM user_thumbnails WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None
