import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'users.db')

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )""")
        conn.commit()
        conn.close()

class User:
    @staticmethod
    def get_by_email(email):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, email, password_hash FROM users WHERE email=?", (email,))
        row = c.fetchone()
        conn.close()
        if row:
            return User(row[1], row[2], row[0])
        return None

    @staticmethod
    def create(email, password):
        password_hash = generate_password_hash(password)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password_hash) VALUES (?,?)", (email, password_hash))
        conn.commit()
        conn.close()
        return User(email, password_hash)

    def __init__(self, email, password_hash, id=None):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
