import unittest
from unittest.mock import MagicMock
import tkinter as tk
from models.notifications import Notifications_System
from ui.notifications_screen import NotificationsScreen

class TestNotificationsSystem(unittest.TestCase):
    def setUp(self):
        # Set up a mock DB cursor
        self.mock_cursor = MagicMock()
        self.ns = Notifications_System(self.mock_cursor)

        # Create a fake root window for tkinter
        self.root = tk.Tk()
        self.root.withdraw()  # Hide root window during tests
        self.user_id = 1

        # Simulate some notifications returned from DB
        self.fake_notifications = [
            (101, "Team Meeting", "alice"),
            (102, "Project Review", "bob")
        ]

    def tearDown(self):
        self.root.destroy()

    def test_notifications_are_suppressed_when_muted(self):
        self.mock_cursor.fetchall.return_value = self.fake_notifications
        self.ns.notifications_muted = True

        notifications = self.ns.get_notifications(self.user_id)

        self.assertEqual(notifications, [])

    def test_notifications_returned_when_not_muted(self):
        self.mock_cursor.fetchall.return_value = self.fake_notifications
        self.ns.notifications_muted = False

        notifications = self.ns.get_notifications(self.user_id)

        self.assertEqual(notifications, self.fake_notifications)

    def test_toggle_mute_from_ui(self):
        screen = NotificationsScreen(self.root, self.ns, self.user_id)

        screen.mute_var.set(True)
        screen.toggle_mute()
        self.assertTrue(self.ns.notifications_muted)

        screen.mute_var.set(False)
        screen.toggle_mute()
        self.assertFalse(self.ns.notifications_muted)

if __name__ == "__main__":
    unittest.main()
