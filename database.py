
import sqlite3
from werkzeug.security import generate_password_hash


def get_db_connection():
    conn = sqlite3.connect("waitless.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():

    conn = get_db_connection()

    # STUDENTS TABLE

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # DOCUMENTS TABLE

    conn.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT NOT NULL,
            filename TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # PRINT REQUESTS TABLE

    conn.execute("""
        CREATE TABLE IF NOT EXISTS print_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT NOT NULL,
            document_id INTEGER NOT NULL,
            copies INTEGER NOT NULL,
            print_type TEXT NOT NULL,
            paper_size TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ADMINS TABLE

    conn.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # CREATE DEFAULT ADMIN

    admin = conn.execute(
        "SELECT id FROM admins WHERE username = ?",
        ("admin",)
    ).fetchone()

    if admin is None:

        hashed_password = generate_password_hash("admin123")

        conn.execute(
            """
            INSERT INTO admins (username, password)
            VALUES (?, ?)
            """,
            ("admin", hashed_password)
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")
