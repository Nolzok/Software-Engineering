# -*- coding: utf-8 -*-
import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk

from ui.Donations import show_reviews_screen 


class TestReviewsScreen(unittest.TestCase):

    @patch('ui.Donations.connect_to_mysql')
    def test_show_reviews_with_data(self, mock_connect):
        mock_conn_1 = MagicMock()
        mock_cursor_1 = MagicMock()
        mock_cursor_1.fetchone.return_value = ("maria_k", 1)

        mock_conn_2 = MagicMock()
        mock_cursor_2 = MagicMock()
        mock_cursor_2.fetchall.return_value = [
            ("test", "test"),
            ("test", "test")
        ]

        mock_connect.side_effect = [
            (mock_conn_1, mock_cursor_1),
            (mock_conn_2, mock_cursor_2),
        ]

        root = tk.Tk()
        root.withdraw()

        try:
            show_reviews_screen(parent=root)
        except Exception as e:
            self.fail(f"Exception raised during GUI execution: {e}")
        finally:
            root.destroy()

        self.assertEqual(mock_connect.call_count, 2)
        mock_cursor_1.execute.assert_called_once_with(
            "SELECT username, user_id FROM users WHERE user_id = 1"
        )
        mock_cursor_2.execute.assert_called_once()
        mock_cursor_2.fetchall.assert_called_once()


if __name__ == "__main__":
    unittest.main()
