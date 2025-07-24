import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'zunekoapp.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea la tabla users si no existe."""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            activo INTEGER NOT NULL DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

class User:
    @staticmethod
    def get_by_email(email):
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = c.fetchone()
        conn.close()
        if row:
            return User(row['id'], row['email'], row['password'], row['activo'])
        return None

    @staticmethod
    def create(email, password, activo=True):
        conn = get_db()
        c = conn.cursor()
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (email, password, activo) VALUES (?, ?, ?)', (email, hashed_password, int(activo)))
        conn.commit()
        conn.close()
        return User.get_by_email(email)

    def __init__(self, id, email, password_hash, activo):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.activo = activo

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
