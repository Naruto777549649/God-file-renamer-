import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                state TEXT,
                filename TEXT,
                thumbnail TEXT
            )
        """)
        self.conn.commit()

    def set_user_state(self, user_id, state):
        self.cur.execute("INSERT OR REPLACE INTO users (user_id, state) VALUES (?, ?)", (user_id, state))
        self.conn.commit()

    def get_user_state(self, user_id):
        self.cur.execute("SELECT state FROM users WHERE user_id=?", (user_id,))
        result = self.cur.fetchone()
        return result[0] if result else None

    def set_filename(self, user_id, filename):
        self.cur.execute("UPDATE users SET filename=? WHERE user_id=?", (filename, user_id))
        self.conn.commit()

    def save_thumbnail(self, user_id, file_id):
        self.cur.execute("UPDATE users SET thumbnail=? WHERE user_id=?", (file_id, user_id))
        self.conn.commit()