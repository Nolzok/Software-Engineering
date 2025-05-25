import unittest
from unittest.mock import MagicMock, patch

from ui.Reviews import submit_points, submit_user_details

class MockEntry:
    """Minimal stand-in for a tk.Entry widget."""
    def __init__(self, value):
        self._value = value
    def get(self):
        return self._value

class TestReviewFunctions(unittest.TestCase):
    @patch('ui.Reviews.selectReviews')          
    @patch('ui.Reviews.connect_to_mysql')
    def test_submit_points_success(self, mock_connect, mock_select):

        mock_conn, mock_cursor = MagicMock(), MagicMock()
        mock_connect.return_value = (mock_conn, mock_cursor)
        mock_cursor.fetchone.return_value = (10,)

        entry = MockEntry("5")

        submit_points(entry, post_required_points=3, client_id=1, post_id=42)

        mock_cursor.execute.assert_any_call(
            "UPDATE pointsystem SET totalpoints = totalpoints - %s WHERE clientID = %s",
            (5, 1)
        )
        mock_cursor.execute.assert_any_call(
            """
            INSERT INTO donation
                (client_id, post_id, date, methodUsed, pointsUsed)
            VALUES (%s, %s, CURDATE(), 'PointExchange', %s)
        """, (1, 42, 5)
        )
        mock_conn.commit.assert_called_once()

    @patch('ui.Reviews.selectReviews')
    @patch('ui.Reviews.connect_to_mysql')
    def test_submit_points_insufficient_raises(self, mock_connect, mock_select):

        mock_conn, mock_cursor = MagicMock(), MagicMock()
        mock_connect.return_value = (mock_conn, mock_cursor)
        mock_cursor.fetchone.return_value = (2,)

        entry = MockEntry("5")

        with self.assertRaises(ValueError):
            submit_points(entry, post_required_points=3, client_id=1, post_id=42)
        mock_conn.commit.assert_not_called()

    @patch('ui.Reviews.connect_to_mysql')
    def test_submit_user_details_username_mismatch(self, mock_connect):

        mock_conn, mock_cursor = MagicMock(), MagicMock()
        mock_connect.return_value = (mock_conn, mock_cursor)
        mock_cursor.fetchone.return_value = ("otheruser",)

        username_entry = MockEntry("maria_k")
        code16_entry   = MockEntry("1111222233334444")
        code3_entry    = MockEntry("123")
        amount_entry   = MockEntry("10")

        submit_user_details(
            username_entry,
            code16_entry,
            code3_entry,
            amount_entry,
            client_id=1,
            post_id=1
        )


        self.assertFalse(
            any("INSERT INTO donation" in call[0][0]
                for call in mock_cursor.execute.call_args_list),
            "No donation INSERT should occur when username mismatches"
        )

if __name__ == "__main__":
    unittest.main()
