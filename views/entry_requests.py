import sqlite3
from models import Entry, Mood, EntryTag, Tag


def get_all_entries():
    """Gets all entries"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.date,
            e.mood_id,
            e.entry,
            m.label
        FROM Entry e
        JOIN Mood m
            ON m.id = e.mood_id
        """)

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['date'], row['mood_id'],
                            row['entry'])
            
            mood = Mood(row['id'], row['label'])
            entry.mood = mood.__dict__

            db_cursor.execute("""
            SELECT
                t.id,
                t.name
            FROM EntryTag et
            JOIN Tag t
                ON t.id = et.tag_id
            WHERE et.entry_id = ?
            """, (entry.id,))

            tags = []
            tag_dataset = db_cursor.fetchall()
            for tag_row in tag_dataset:
                tag = Tag(tag_row['id'], tag_row['name'])
                tags.append(tag.__dict__)

            entry.tags = tags

            entries.append(entry.__dict__)

    return entries

def get_single_entry(id):
    """Gets single entry by id"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.date,
            e.mood_id,
            e.entry
        FROM 'Entry' e
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'], data['date'], data['mood_id'],
                            data['entry'])

        return entry.__dict__

def get_entries_by_search(searched_term):
    """Gets entires by searched term"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                e.id,
                e.concept,
                e.date,
                e.mood_id,
                e.entry
            from Entry e
            WHERE e.concept LIKE ?
            """, (f'%{searched_term}%',))


        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['date'], row['mood_id'] , row['entry'])
            entries.append(entry.__dict__)

    return entries

def delete_entry(id):
    """Deletes single entry by id"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM 'Entry'
        WHERE id = ?
        """, (id, ))

def create_journal_entries(new_entry):
    """Creates a new entry"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entry
            ( concept, date, mood_id, entry )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_entry['concept'], new_entry['date'],
            new_entry['mood_id'], new_entry['entry'],))

        id = db_cursor.lastrowid
        new_entry['id'] = id

        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO EntryTag
                ( entry_id, tag_id )
            VALUES
                ( ?, ? );
            """, (new_entry['id'], tag))

    return new_entry

def update_entry(id, new_entry):
    """Updates entry with client information"""

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entry
            SET
                concept = ?,
                entry = ?,
                date = ?,
                mood_id = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'],
            new_entry['date'], new_entry['mood_id'], id, ))
        
        rows_affected = db_cursor.rowcount
        if rows_affected == 0:
            return False
        else:
            return True