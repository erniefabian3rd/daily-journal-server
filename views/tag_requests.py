import sqlite3
from models import Tag

def get_all_tags():
    """Gets all tags"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM Tag t
        """)

        tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['name'] )

            tags.append(tag.__dict__)

    return tags

def get_single_tag(id):
    """Gets single tag by id"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM Tag t
        WHERE t.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        tag = Tag(data['id'], data['name'])

        return tag.__dict__