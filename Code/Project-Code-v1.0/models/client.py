from models.points_system import PointsSystem
from models.redemption import Redemption


class Client:
    def __init__(self, name="Χρήστης"):
        self.name = name
        self.points_system = PointsSystem()
        self.redemptions = []

    def choose_category(self, root, category):
        from ui.category_screen import show_category_screen
        show_category_screen(root, self, category)

    def make_selection(self, category, option):
        if option in {
            "VIP Πρόσκληση",
            "Ειδικό Αναμνηστικό Δώρο"
        }:
            return {"status": "expired", "message": f"Η ανταμοιβή '{option}' έχει λήξει."}
        
        return {"status": "valid"}

    def choose_redemption(self, root):
        from ui.categories_screen import show_categories_screen
        show_categories_screen(root, self)
        
    def select_profile_icon(self):
        print("User clicked Profile Icon")

    def choose_edit_profile_button(self):
        print("User selected to edit profile")

    def modify_data(self, new_data):
        print("User modifies profile data")

    def choose_exit(self):
        print("User exits without saving")
