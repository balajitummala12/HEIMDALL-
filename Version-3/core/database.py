import sqlite3
import os

DB_NAME = os.path.join("data", "memory.db")


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS conversations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS profile(
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS study_topics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT,
        topic TEXT,
        status TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS image_memories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        extracted_text TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

    # ===============================
    # Conversation Memory
    # ===============================

    def save_message(role, content):
        conn = get_connection()

        conn.execute(
            """
            INSERT INTO conversations(role, content)
            VALUES (?, ?)
            """,
            (role, content)
        )

        conn.commit()
        conn.close()

    def load_memory(limit=10):
        conn = get_connection()

        rows = conn.execute(
            """
            SELECT role, content
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        ).fetchall()

        conn.close()

        rows.reverse()

        return [
            {"role": role, "content": content}
            for role, content in rows
        ]

    # ===============================
    # Profile Memory
    # ===============================

    def save_profile(key, value):
        conn = get_connection()

        conn.execute(
            """
            INSERT OR REPLACE INTO profile(key, value)
            VALUES (?, ?)
            """,
            (key, value)
        )

        conn.commit()
        conn.close()

    def get_profile(key):
        conn = get_connection()

        row = conn.execute(
            """
            SELECT value
            FROM profile
            WHERE key=?
            """,
            (key,)
        ).fetchone()

        conn.close()

        return row[0] if row else None

    # ===============================
    # Study Tracker
    # ===============================

    def save_topic(subject, topic):
        conn = get_connection()

        conn.execute(
            """
            INSERT INTO study_topics(subject, topic, status)
            VALUES (?, ?, ?)
            """,
            (subject, topic, "Completed")
        )

        conn.commit()
        conn.close()

    def load_topics():
        conn = get_connection()

        rows = conn.execute(
            """
            SELECT subject, topic
            FROM study_topics
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        return rows

    # ===============================
    # Image Memory
    # ===============================

    def save_image_memory(image_name, extracted_text):
        conn = get_connection()

        conn.execute(
            """
            INSERT INTO image_memories(image_name, extracted_text)
            VALUES (?, ?)
            """,
            (image_name, extracted_text)
        )

        conn.commit()
        conn.close()

    def load_image_memories():
        conn = get_connection()

        rows = conn.execute(
            """
            SELECT image_name, extracted_text
            FROM image_memories
            ORDER BY id DESC
            """
        ).fetchall()

        conn.close()

        return rows

    # ===============================
    # Database Stats
    # ===============================

    def get_memory_count():
        conn = get_connection()

        count = conn.execute(
            "SELECT COUNT(*) FROM conversations"
        ).fetchone()[0]

        conn.close()

        return count