class Redemption:
    def __init__(self, redemption_id, category, selected_option):
        self.id = redemption_id
        self.category = category
        self.selected_option = selected_option
        self.is_completed = False

    def redeem_points(self):
        self.is_completed = True
        print(f"Εξαργυρώθηκε η επιλογή: {self.selected_option}")