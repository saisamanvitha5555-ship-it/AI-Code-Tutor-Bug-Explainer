import sqlite3


DATABASE_NAME = "code_history.db"


def create_database():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        language TEXT NOT NULL,

        code TEXT NOT NULL,

        analysis TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def save_history(language, code, analysis):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO history
    (
        language,
        code,
        analysis
    )
    VALUES (?, ?, ?)
    """,
    (
        language,
        code,
        analysis
    ))

    conn.commit()
    conn.close()


def get_history():

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        language,
        code,
        analysis,
        created_at
    FROM history
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_history(record_id):

    conn = sqlite3.connect(DATABASE_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE id = ?",
        (record_id,)
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_database()

    print("Database created successfully.")