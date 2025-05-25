import unittest
from unittest.mock import patch, MagicMock
from models.organizer import Organizer
from models.event import Event
from datetime import datetime


class TestOrganizer(unittest.TestCase):

    def setUp(self):
        self.organizer = Organizer(organizer_id=1, name="Test Organizer")

    def test_add_event_returns_empty_fields(self):
        event_data = self.organizer.add_event()
        self.assertIsInstance(event_data, dict)
        self.assertEqual(event_data["name"], "")
        self.assertEqual(event_data["max_participants"], 0)

    def test_fill_form_valid_data(self):
        form_data = {
            "name": "Test Event",
            "location": "Athens",
            "date": "25/12/2025 18:00",
            "max_participants": 100,
            "category": "Technology",
            "price": 20.0,
            "duration": 90,
            "description": "Sample description"
        }

        event = self.organizer.fill_form(form_data)
        self.assertIsInstance(event, Event)
        self.assertEqual(event.name, "Test Event")
        self.assertEqual(event.date, datetime(2025, 12, 25, 18, 0))

    def test_fill_form_invalid_date(self):
        form_data = {
            "name": "Invalid Date Event",
            "location": "Athens",
            "date": "invalid-date",
            "max_participants": 50,
            "category": "Art",
            "price": 15.0,
            "duration": 60,
            "description": "Error date"
        }
        event = self.organizer.fill_form(form_data)
        self.assertIsNone(event)

    def test_save_and_cancel_draft(self):
        dummy_event = MagicMock()
        self.organizer.save_form(dummy_event)
        self.assertIn(dummy_event, self.organizer.drafts)

        self.organizer.cancel_event(dummy_event)
        self.assertNotIn(dummy_event, self.organizer.drafts)

    @patch("models.organizer.connect_to_mysql")
    def test_submit_event_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = (mock_conn, mock_cursor)

        dummy_event = Event(
            name="Mock Event",
            date=datetime.now(),
            location="Mock Location",
            max_participants=100,
            category="Mock",
            price=10.0,
            duration=60,
            description="Mock description",
            organizer_id=1
        )

        success = self.organizer.submit_event(dummy_event)
        self.assertTrue(success)
        self.assertIn(dummy_event, self.organizer.events)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch("models.organizer.connect_to_mysql", side_effect=Exception("DB Error"))
    def test_submit_event_failure(self, mock_connect):
        dummy_event = Event(
            name="Fail Event",
            date=datetime.now(),
            location="Anywhere",
            max_participants=50,
            category="Fail",
            price=0.0,
            duration=30,
            description="Failure",
            organizer_id=1
        )
        success = self.organizer.submit_event(dummy_event)
        self.assertFalse(success)
        self.assertNotIn(dummy_event, self.organizer.events)


if __name__ == "__main__":
    unittest.main()
