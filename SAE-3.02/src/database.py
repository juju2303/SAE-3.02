import sqlite3
from datetime import datetime
from pathlib import Path


class Database:
    def __init__(self):
        database_folder = (Path(__file__).parent.parent / "database")
        database_folder.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(database_folder / "traffic.db")
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                type TEXT,
                message TEXT
            )
        """)
        self.connection.commit()

    def add_event(self,event_type,message):
        self.connection.execute(
            """
            INSERT INTO events(
                date,
                type,
                message
            )
            VALUES (?, ?, ?)
            """,
            (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                event_type,
                message
            )
        )
        self.connection.commit()

    def close(self):
        self.connection.close()