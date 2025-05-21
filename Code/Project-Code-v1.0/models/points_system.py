class PointsSystem:
    def __init__(self):
        self.total_points = 0
        self.extra_points = 0

    def calculate_points(self):
        self.total_points += self.extra_points
        print("Υπολογίστηκαν οι πόντοι.")

    def show_points(self):
        print(f"Πόντοι: {self.total_points}")
        return self.total_points

    def check_balance(self):
        return self.total_points >= 50

    def deduct_points(self, amount):
        if self.total_points >= amount:
            self.total_points -= amount
            return True
        return False
