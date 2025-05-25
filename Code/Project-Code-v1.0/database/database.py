import mysql.connector
import sqlite3    

from dataclasses import dataclass
from database.db_config import DB_CONFIG

def connect_to_mysql():
    """
    Returns a (conn, cursor) tuple connected to your MySQL database.
    """
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='database_password',
        database='software_engineering'
    )
    cursor = conn.cursor()
    return conn, cursor


 
def get_connection(db_type='mysql'):
    """
    If db_type == 'mysql', returns (conn, cursor) for MySQL.
    If db_type == 'sqlite', returns (conn, cursor) for SQLite.
    """
    if db_type == 'sqlite':
        conn = sqlite3.connect('my_local.db')
        cursor = conn.cursor()
        return conn, cursor
    else:
        return connect_to_mysql()

@dataclass
class ProfileData:
    name: str = ""
    email: str = ""
    phone_number: str = ""
    address: str = ""
    bio: str = ""
    friendCode: str = ""
    friends: str = "0"


class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='database_password',
            database='software_engineering'
        )
        self.cursor = self.connection.cursor()

    def fetch_profile_data(self):
        self.cursor.execute("""
            SELECT 
                c.cl_name,
                u.email,
                u.phone,
                p.address,
                p.bio,
                c.friendcode,
                COALESCE(p.friends, '0') as friends
            FROM clients c
            JOIN users u ON c.clientID = u.user_id
            JOIN profile p ON c.clientID = p.id
            WHERE c.clientID = 1
            LIMIT 1
        """)
        result = self.cursor.fetchone()
        if result:
            return ProfileData(
                name=result[0],
                email=result[1],
                phone_number=result[2],
                address=result[3],
                bio=result[4],
                friendCode=result[5],
                friends=result[6]
            )
        return ProfileData()

    def fetch_friends_count(self):
        return "0"   

    def update_profile(self, profile_data):
         
        self.cursor.execute("""
            UPDATE users u
            JOIN clients c ON u.user_id = c.clientID
            SET u.email = %s, u.phone = %s, u.username = %s
            WHERE c.clientID = 1
        """, (profile_data.email, profile_data.phone_number, profile_data.name))

         
        self.cursor.execute("""
            UPDATE clients 
            SET cl_name = %s, friendcode = %s
            WHERE clientID = 1
        """, (profile_data.name, profile_data.friendCode))

         
        self.cursor.execute("""
            UPDATE profile 
            SET address = %s, bio = %s, friends = %s
            WHERE id = 1
        """, (profile_data.address, profile_data.bio, profile_data.friends))

        self.connection.commit()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()





class Database_2:
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
         
        return True

    def release_seat(self, seat_number):
         
         
        return True

    def save_data(self, form):
        query = """
            INSERT INTO participation_form 
            (full_name, age, phone, email, interests, dietary_preferences, special_requests, accepted_terms, event_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            age = int(form.age)   
            values = (
                form.full_name,
                age,
                form.phone_number,
                form.email,
                form.interests,
                form.dietary_preferences,
                form.special_needs,
                1,   
                1    
            )
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except (ValueError, mysql.connector.Error) as err:
            print(f"Database Error: {err}")
            self.conn.rollback()
            return False

    def get_event_details(self, event_id=1):   
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
