import sqlite3
from pathlib import Path

# Locate the project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Database file path
DB_PATH = PROJECT_ROOT / "lifeos.db"


def get_connection():
    """Create a connection to the SQLite database."""

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the tasks table if it doesn't exist."""

    with get_connection() as connection:

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                priority TEXT NOT NULL DEFAULT 'Medium',
                duration INTEGER NOT NULL DEFAULT 30,
                deadline TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )


def add_task(title, priority, duration, deadline, created_at):
    """Insert a new task into the database."""

    with get_connection() as connection:

        connection.execute(
            """
            INSERT INTO tasks (
                title,
                priority,
                duration,
                deadline,
                completed,
                created_at
            )
            VALUES (?, ?, ?, ?, 0, ?)
            """,
            (
                title,
                priority,
                duration,
                deadline,
                created_at,
            ),
        )


def get_tasks():
    """Retrieve all tasks from the database."""

    with get_connection() as connection:

        rows = connection.execute(
            """
            SELECT *
            FROM tasks
            ORDER BY deadline ASC, id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def update_task_status(task_id, completed):
    """Update the completion status of a task."""

    with get_connection() as connection:

        connection.execute(
            """
            UPDATE tasks
            SET completed = ?
            WHERE id = ?
            """,
            (int(completed), task_id),
        )


def delete_task(task_id):
    """Delete a task using its database ID."""

    with get_connection() as connection:

        connection.execute(
            """
            DELETE FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        )