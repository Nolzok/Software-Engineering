from models.points_system import PointsSystem

class Client:
    def __init__(self, name):
        self.name = name
        self.points_system = PointsSystem()
        self.redemptions = []

    def choose_redemption(self):
        print(f"{self.name} επέλεξε εξαργύρωση.")
