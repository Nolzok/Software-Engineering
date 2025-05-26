from models.event import Event
from datetime import datetime
from db.database import connect_to_mysql


class Organizer:
    def __init__(self, organizer_id: int, name: str):
        self.organizer_id = organizer_id
        self.name = name
        self.events = []  
        self.drafts = []  

    def add_event(self):
        return {
            "name": "",
            "location": "",
            "date": "",  
            "max_participants": 0,
            "category": "",
            "price": 0.0,
            "duration": 0,
            "description": ""
        }

    def fill_form(self, form_data: dict):
        try:
            form_data["date"] = datetime.strptime(form_data["date"], "%d/%m/%Y %H:%M")
        except Exception as e:
            print("Λάθος ημερομηνία:", e)
            return None

        event = Event(
            name=form_data["name"],
            location=form_data["location"],
            date=form_data["date"],
            max_participants=form_data["max_participants"],
            category=form_data["category"],
            price=form_data["price"],
            duration=form_data["duration"],
            description=form_data["description"],
            organizer_id=self.organizer_id
        )
        return event

    def save_form(self, event_draft):
        self.drafts.append(event_draft)

    def cancel_event(self, event_draft):
        if event_draft in self.drafts:
            self.drafts.remove(event_draft)

    def submit_event(self, event):
        try:
            conn, cursor = connect_to_mysql()
            insert_query = """
                INSERT INTO events 
                (name, location, datetime, maxParticipants, category, price, duration, details, organizerID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                event.name,
                event.location,
                event.date.strftime("%Y-%m-%d %H:%M:%S"),
                event.max_participants,
                event.category,
                event.price,
                event.duration,
                event.description,
                self.organizer_id
            ))
            conn.commit()
            cursor.close()
            conn.close()
            self.events.append(event)
            return True
        except Exception as e:
            print(f"DB error: {e}")
            return False
