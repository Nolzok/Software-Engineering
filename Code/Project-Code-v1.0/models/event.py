from datetime import datetime

class Event:
    def __init__(self, name: str, date: datetime,
                 location: str = "", max_participants: int = 0,
                 category: str = "", price: float = 0.0,
                 duration: int = 0, description: str = "",
                 event_id: str = None, rating: float = 0.0,
                 organizer_id: int = None):
        self.name = name
        self.date = date
        self.location = location
        self.max_participants = max_participants
        self.category = category
        self.price = price
        self.duration = duration
        self.description = description

        self.event_id = event_id
        self.rating = rating
        self.organizer_id = organizer_id

    def display_details_of_event(self):
        return {
            "name": self.name,
            "date": self.date,
            "location": self.location,
            "max_participants": self.max_participants,
            "category": self.category,
            "price": self.price,
            "duration": self.duration,
            "description": self.description,
            "rating": self.rating
        }
