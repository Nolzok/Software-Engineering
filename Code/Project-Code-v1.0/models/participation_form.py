from controllers.validators import validate_form


class ParticipationForm:
    def __init__(self, seat_number, event_id):
        self.seat_number = seat_number
        self.event_id = event_id
        self.full_name = ""
        self.age = 0
        self.phone_number = ""
        self.email = ""
        self.interests = ""
        self.dietary_preferences = ""
        self.special_needs = ""

    def press_submit(self):
        if validate_form(self):
            return "ok"
        return "missing"
