import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'zunekoapp.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea la tabla users si no existe y agrega is_active si falta."""
    conn = get_db()
    c = conn.cursor()
    # Crear tabla si no existe
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_active INTEGER NOT NULL DEFAULT 1
        )
    ''')
    # Asegurar columna is_active si la tabla existía sin ella
    try:
        c.execute('ALTER TABLE users ADD COLUMN is_active INTEGER NOT NULL DEFAULT 1')
    except sqlite3.OperationalError:
        # Ya existe la columna, no hacer nada
        pass
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
            return User(row['id'], row['email'], row['password'], row['is_active'])
        return None

    @staticmethod
    def create(email, password, is_active=1):
        conn = get_db()
        c = conn.cursor()
        hashed_password = generate_password_hash(password)
        c.execute('INSERT INTO users (email, password, is_active) VALUES (?, ?, ?)', (email, hashed_password, is_active))
        conn.commit()
        conn.close()
        return User.get_by_email(email)

    def __init__(self, id, email, password_hash, is_active):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.is_active = is_active

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
