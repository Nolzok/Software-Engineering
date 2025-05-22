class Organizer:
    def __init__(self, organizer_id: int, name: str):
        self.organizer_id = organizer_id
        self.name = name
        self.events = []  
        self.event_creations = []  

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
        from models.event_creation import EventCreation
        event = EventCreation(**form_data)
        return event

    def save_form(self, event_creation):
        
        self.event_creations.append(event_creation)

    def cancel_event(self, event_creation):
        
        if event_creation in self.event_creations:
            self.event_creations.remove(event_creation)

    def submit_event(self, event_creation, event_service):
        
        if event_service.validate(event_creation):
            saved_event = event_service.final_save(event_creation, self.organizer_id)
            if saved_event:
                self.events.append(saved_event)
                if event_creation in self.event_creations:
                    self.event_creations.remove(event_creation)
                return saved_event
        return None
