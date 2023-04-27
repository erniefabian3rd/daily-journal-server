import sqlite3
from models import EntryTag

def get_all_entry_tags():
    """Gets all entry tags"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id
        FROM EntryTag et
        """)

        entry_tags = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry_tag = EntryTag(row['id'], row['entry_id'], row['tag_id'] )

            entry_tags.append(entry_tag.__dict__)

    return entry_tags

def get_single_entry_tag(id):
    """Gets single entry tag by id"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id
        FROM EntryTag et
        WHERE et.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        entry_tag = EntryTag(data['id'], data['entry_id'], data['tag_id'])

        return entry_tag.__dict__