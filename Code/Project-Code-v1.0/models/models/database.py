import mysql.connector
from config.db_config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def check_available_seats(self, event_id):
        query = """
            SELECT e.maxParticipants,
                   (SELECT COUNT(*) FROM participation_form WHERE event_id = %s) as booked_seats
            FROM events e 
            WHERE e.eventID = %s
        """
        self.cursor.execute(query, (event_id, event_id))
        result = self.cursor.fetchone()
        if result:
            return result['maxParticipants'] - result['booked_seats']
        return 0

    def temp_booked_seats(self, seat_number):
        # Implement temporary booking logic
        return True

    def release_seat(self, seat_number):
        # Since we're not actually storing temporary seats in database,
        # we just need this method to exist for the timeout handler
        return True

    def save_data(self, form):
        query = """
            INSERT INTO participation_form 
            (full_name, age, phone, email, interests, dietary_preferences, special_requests, accepted_terms, event_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            age = int(form.age)  # Age should already be validated
            values = (
                form.full_name,
                age,
                form.phone_number,
                form.email,
                form.interests,
                form.dietary_preferences,
                form.special_needs,
                1,  # accepted_terms
                1   # event_id
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except (ValueError, mysql.connector.Error) as err:
            print(f"Database Error: {err}")
            self.conn.rollback()
            return False

    def get_event_details(self, event_id=1):  # Default to first event
        query = """
            SELECT eventID as id, name, location, datetime, 
                   maxParticipants, category, price 
            FROM events 
            WHERE eventID = %s
        """
        self.cursor.execute(query, (event_id,))
        return self.cursor.fetchone() or {'id': 1, 'name': 'No event', 'maxParticipants': 0}

    def get_event_seats(self, event_id):
        query = """
            SELECT e.maxParticipants,
                   (SELECT COUNT(*) FROM participation_form WHERE event_id = %s) as booked
            FROM events e
            WHERE e.eventID = %s
        """
        self.cursor.execute(query, (event_id, event_id))
        result = self.cursor.fetchone()
        if result:
            return {
                'total': result['maxParticipants'],
                'available': result['maxParticipants'] - result['booked']
            }
        return {'total': 0, 'available': 0}

    def get_events(self):
        query = """
            SELECT eventID as id, name, location, datetime, maxParticipants, category, price, duration, details
            FROM events
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def __del__(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
