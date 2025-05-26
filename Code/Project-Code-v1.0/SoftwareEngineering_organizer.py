from ui.events_screen import EventsScreen
from ui.form_screen import FormScreen
from models.organizer import Organizer


if __name__ == "__main__":
    organizer = Organizer(organizer_id=4, name="Χρήστης")  
    app = EventsScreen(organizer=organizer, form_screen_class=FormScreen)  
    app.mainloop()
