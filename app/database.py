"""
database.py
Handles SQLite connection and schema creation for the IT Helpdesk System.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "helpdesk.db")


def get_connection():
    """Return a connection to the SQLite database with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS technicians (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    level TEXT NOT NULL CHECK (level IN ('L1', 'L2', 'L3'))
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL CHECK (type IN ('Incident', 'Service Request')),
    category TEXT,
    impact TEXT NOT NULL CHECK (impact IN ('Low', 'Medium', 'High')),
    urgency TEXT NOT NULL CHECK (urgency IN ('Low', 'Medium', 'High')),
    priority TEXT NOT NULL CHECK (priority IN ('Low', 'Medium', 'High', 'Critical')),
    status TEXT NOT NULL DEFAULT 'Open' CHECK (status IN ('Open', 'In Progress', 'Escalated', 'Resolved', 'Closed')),
    assigned_to INTEGER,
    created_at TEXT NOT NULL,
    resolved_at TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (assigned_to) REFERENCES technicians(id)
);

CREATE TABLE IF NOT EXISTS ticket_updates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER NOT NULL,
    technician_id INTEGER,
    note TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id),
    FOREIGN KEY (technician_id) REFERENCES technicians(id)
);
"""


def init_db():
    """Create all tables if they do not already exist."""
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def reset_db():
    """Drop and recreate all tables. Useful for reseeding demo data."""
    conn = get_connection()
    conn.executescript("""
        DROP TABLE IF EXISTS ticket_updates;
        DROP TABLE IF EXISTS tickets;
        DROP TABLE IF EXISTS technicians;
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS departments;
    """)
    conn.commit()
    conn.close()
    init_db()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
