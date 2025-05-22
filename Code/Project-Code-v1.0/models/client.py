from models.points_system import PointsSystem

class Client:
    def __init__(self, name="DefaultUser", profile=None):
        self.name = name
        self.profile = profile
        self.points_system = PointsSystem()
        self.redemptions = []

    def choose_redemption(self):
        print(f"{self.name} επέλεξε εξαργύρωση.")
    def select_profile_icon(self):
        print("User clicked Profile Icon")

    def choose_edit_profile_button(self):
        print("User selected to edit profile")

    def modify_data(self, new_data):
        print("User modifies profile data")

    def choose_exit(self):
        print("User exits without saving")
