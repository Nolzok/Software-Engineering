import unittest
from models.profile import Profile

class TestProfileModel(unittest.TestCase):
    def setUp(self):
        self.profile = Profile(
            name="John Doe",
            email="john@example.com",
            phoneNumber="1234567890",
            address="123 Main St",
            bio="Hello, I'm John.",
            friend_code="ABC123",
            friends=["Alice", "Bob"]
        )

    def test_initialization(self):
        self.assertEqual(self.profile.name, "John Doe")
        self.assertEqual(self.profile.email, "john@example.com")
        self.assertEqual(self.profile.phoneNumber, "1234567890")
        self.assertEqual(self.profile.address, "123 Main St")
        self.assertEqual(self.profile.bio, "Hello, I'm John.")
        self.assertEqual(self.profile.friend_code, "ABC123")
        self.assertEqual(self.profile.friends, ["Alice", "Bob"])

    def test_update_profile(self):
        self.profile.update_profile("Jane Doe", "jane@example.com", "0987654321", "456 Main St", "Updated bio")
        self.assertEqual(self.profile.name, "Jane Doe")
        self.assertEqual(self.profile.email, "jane@example.com")
        self.assertEqual(self.profile.phoneNumber, "0987654321")
        self.assertEqual(self.profile.address, "456 Main St")
        self.assertEqual(self.profile.bio, "Updated bio")
