import unittest
from unittest.mock import MagicMock
import tkinter as tk
from ui.Friendspage import FriendsPage  # Adjust if module path differs
from models.Friends_System import FriendsSystem

class TestFriendsSystemAndUI(unittest.TestCase):
    def setUp(self):
        self.mock_fs = MagicMock()
        self.root = tk.Tk()
        self.root.withdraw()
        self.current_user = 1
        self.page = FriendsPage(self.root, self.mock_fs, self.current_user)

    def tearDown(self):
        self.root.destroy()

    def test_send_request_calls_backend(self):
        self.page.send_request(2)
        self.mock_fs.send_friend_request.assert_called_with(1, 2)

    def test_refresh_friends_displays_labels(self):
        self.mock_fs.get_friends.return_value = [(2, "alice"), (3, "bob")]
        self.page.refresh_friends()
        children = self.page.friends_list.winfo_children()
        self.assertEqual(len(children), 2)

    def test_refresh_pending_displays_sent_request(self):
        self.mock_fs.get_pending_requests.return_value = [(1, 2, "bob")]
        self.page.refresh_pending()
        children = self.page.pending_list.winfo_children()
        self.assertEqual(len(children), 1)
        self.assertIn("bob", children[0].winfo_children()[0]['text'])

    def test_refresh_pending_displays_received_request(self):
        self.mock_fs.get_pending_requests.return_value = [(2, 1, "alice")]
        self.page.refresh_pending()
        children = self.page.pending_list.winfo_children()
        self.assertEqual(len(children), 1)
        buttons = [w for w in children[0].winfo_children() if isinstance(w, tk.Button)]
        self.assertEqual(len(buttons), 2)  # Accept + Reject buttons

    def test_respond_calls_backend_update(self):
        self.page.respond(2, 1, "accepted")
        self.mock_fs.update_friend_request_status.assert_called_with(2, 1, "accepted")

if __name__ == "__main__":
    unittest.main()

