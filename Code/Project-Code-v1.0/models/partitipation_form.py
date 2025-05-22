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

    def fill_form(self):
        # Προσομοίωση συμπλήρωσης από τον χρήστη
        self.full_name = input("Full name: ")
        self.age = int(input("Age: "))
        self.phone_number = input("Phone number: ")
        self.email = input("Email: ")
        self.interests = input("Interests: ")
        self.dietary_preferences = input("Dietary preferences: ")
        self.special_needs = input("Special needs: ")

    def press_submit(self):
        from utils.validators import validate_form
        if not validate_form(self):
            return "missing"
        return "ok"

    def complete_participation(self):
        print("Participation completed.")
