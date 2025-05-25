import unittest
from unittest.mock import MagicMock
import tkinter as tk
from ui.lostItems import LostItemsApp   

class TestLostItemsApp(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  
        self.app = LostItemsApp(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_validate_phone_valid(self):
        self.assertTrue(self.app.validate_phone("6981234567"))

    def test_validate_phone_too_short(self):
        self.assertFalse(self.app.validate_phone("698123"))

    def test_validate_phone_too_long(self):
        self.assertFalse(self.app.validate_phone("698123456789"))

    def test_validate_phone_letters(self):
        self.assertFalse(self.app.validate_phone("69A23B4567"))

    def test_validate_phone_empty(self):
        self.assertFalse(self.app.validate_phone(""))

    def test_validate_phone_spaces(self):
        self.assertFalse(self.app.validate_phone("698 123 4567"))

if __name__ == "__main__":
    unittest.main()