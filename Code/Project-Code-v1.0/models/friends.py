import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import simpledialog


 

class FriendsSystem:
    def __init__(self, db_config):
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor()

    def get_users(self):
        self.cursor.execute("SELECT user_id, username FROM users")
        return self.cursor.fetchall()

    def send_friend_request(self, sender_id, receiver_id):
        self.cursor.execute("""
            SELECT status FROM friends
            WHERE (user_id = %s AND friend_id = %s)
               OR (user_id = %s AND friend_id = %s)
        """, (sender_id, receiver_id, receiver_id, sender_id))
        if self.cursor.fetchone() :
            raise Exception("Friend request already exists or you are already friends.")

        self.cursor.execute(
            "INSERT INTO friends (user_id, friend_id, status) VALUES (%s, %s, %s)",
            (sender_id, receiver_id, "pending")
        )
        self.conn.commit()

    def get_pending_requests(self, user_id):
        self.cursor.execute("""
            SELECT f.user_id, f.friend_id, u.username
            FROM friends f
            JOIN users u ON
                (u.user_id = CASE WHEN f.user_id = %s THEN f.friend_id ELSE f.user_id END)
            WHERE (f.user_id = %s OR f.friend_id = %s)
              AND f.status = 'pending'
        """, (user_id, user_id, user_id))
        return self.cursor.fetchall()

    def update_friend_request_status(self, sender_id, receiver_id, new_status):
     if new_status == "rejected":
        self.cursor.execute("""
            DELETE FROM friends
            WHERE (user_id = %s AND friend_id = %s)
               OR (user_id = %s AND friend_id = %s)
        """, (sender_id, receiver_id, receiver_id, sender_id))
     else:
        self.cursor.execute("""
            UPDATE friends
            SET status = %s
            WHERE (user_id = %s AND friend_id = %s)
               OR (user_id = %s AND friend_id = %s)
        """, (new_status, sender_id, receiver_id, receiver_id, sender_id))
     self.conn.commit()


    def get_friends(self, user_id):
        self.cursor.execute("""
            SELECT u.user_id, u.username
            FROM friends f
            JOIN users u ON (u.user_id = CASE WHEN f.user_id = %s THEN f.friend_id ELSE f.user_id END)
            WHERE (f.user_id = %s OR f.friend_id = %s)
              AND f.status = 'accepted'
        """, (user_id, user_id, user_id))
        return self.cursor.fetchall()
    
    def search_users_by_username(self, query):
     self.cursor.execute(
        "SELECT user_id, username FROM users WHERE username LIKE %s",
        (f"%{query}%",)
     )
     return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()


 
 




 

