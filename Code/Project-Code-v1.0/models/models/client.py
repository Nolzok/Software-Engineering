class Client:
    def select_commitment_button(self, event_screen):
        event_screen.check_available_seats()

    def press_commitment_button(self, commitment_seat_screen):
        commitment_seat_screen.temp_booked_seats()

    def fill_form(self, form):
        form.fill_form()

    def press_submit(self, form):
        form.press_submit()
