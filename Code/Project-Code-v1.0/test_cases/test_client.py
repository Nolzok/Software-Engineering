import unittest
from models.client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        self.client.points_system.total_points = 100  
        self.client.points_system.extra_points = 20
        self.client.redemptions = []

    def test_valid_selection(self):
        result = self.client.make_selection("Τεχνολογία", "Εισιτήριο Γενικής Εισόδου")
        self.assertEqual(result["status"], "valid")
        self.assertEqual(len(self.client.redemptions), 0)  
        self.assertEqual(self.client.points_system.total_points, 100)  

    def test_redemption_expired_option(self):
        result = self.client.make_selection("Τεχνολογία", "VIP Πρόσκληση")
        self.assertEqual(result["status"], "expired")
        self.assertIn("λήξει", result["message"])

    def test_deduct_points_success(self):
        before = self.client.points_system.total_points
        success = self.client.points_system.deduct_points(50)
        self.assertTrue(success)
        self.assertEqual(self.client.points_system.total_points, before - 50)

    def test_deduct_points_fail(self):
        self.client.points_system.total_points = 10
        success = self.client.points_system.deduct_points(50)
        self.assertFalse(success)
        self.assertEqual(self.client.points_system.total_points, 10)

if __name__ == "__main__":
    unittest.main()
