class Event:
    def __init__(self, name, date, event_id, details, rating, categories, organizer_id):
        self.name = name
        self.date = date
        self.event_id = event_id
        self.details = details
        self.rating = rating
        self.category = category
        self.organizer_id = organizer_id
        self.reviews = []

    def load_past_events(self):
        return []

    def display_details_of_events(self):
        print(f"{self.name} - {self.details}")
