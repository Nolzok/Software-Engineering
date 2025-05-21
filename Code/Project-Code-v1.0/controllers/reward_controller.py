from models.client import Client
from models.redemption import Redemption
from ui.points_screen import show_points_screen

class RewardController:
    def __init__(self):
        self.client = Client("Maria")
        self.redemption_id = 0

    def handle_redemption_click(self, root):
        self.client.choose_redemption()
        show_points_screen(root, self)

    def create_redemption(self, category, selected_option):
        self.redemption_id += 1
        redemption = Redemption(self.redemption_id, category, selected_option)
        self.client.redemptions.append(redemption)
        return redemption



#from models.client import Client
#from models.redemption import Redemption
#from ui.points_screen import show_points_screen
#from db.client_repository import get_client_points

##   def __init__(self):
  #      self.client_id = 1  # ή πάρε το από login αργότερα
   #     self.client = self._load_client_from_db()
    #    self.redemption_id = 0

    #def _load_client_from_db(self):
     #   data = get_client_points(self.client_id)

      ##     raise ValueError("Ο χρήστης δεν βρέθηκε στη βάση")
#client = Client("Maria")  # ή χρησιμοποίησε και το όνομα από τη βάση αν το προσθέσεις
 ##      client.points_system.extra_points = data['extra_points']
   #     return client
