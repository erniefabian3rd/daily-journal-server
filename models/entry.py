class Entry():
    """Class to contain all entry fields"""

    def __init__(self, id, concept, date, mood_id, entry=""):
        self.id = id
        self.concept = concept
        self.date = date
        self.mood_id = mood_id
        self.entry = entry
