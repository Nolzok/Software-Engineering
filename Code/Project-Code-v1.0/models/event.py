class Event:
    def __init__(self, name, date, event_id, details, rating, categories, organizer_id):
        self.name = name
        self.date = date
        self.event_id = event_id
        self.details = details
        self.rating = rating
        self.categories = categories
        self.organizer_id = organizer_id
        self.reviews = []

    def get_reviews(self):
        return self.reviews

    def load_past_events(self):
        # Θα επιστρέψει dummy δεδομένα
        return []

    def add_review(self, review):
        self.reviews.append(review)

    def display_details_of_events(self):
        print(f"{self.name} - {self.details}")
