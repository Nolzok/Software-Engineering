class Notifications_System:
    def __init__(self, cursor):
        self.cursor = cursor
        self.has_notifications = False
        self.notifications_muted =  False 

    def update_notifications_status(self, user_id):
        if self.notifications_muted:
            self.has_notifications = False
            return

        self.cursor.execute("""
            SELECT 1 FROM assigned_event ae
            JOIN friends f ON ((f.user_id = %s AND f.friend_id = ae.user_id) OR (f.friend_id = %s AND f.user_id = ae.user_id))
            WHERE f.status = 'accepted' AND ae.user_id != %s
            LIMIT 1
        """, (user_id, user_id, user_id))
        result = self.cursor.fetchone()
        self.has_notifications = bool(result)

    def get_notifications(self, user_id):
        if self.notifications_muted:
            return []

        self.cursor.execute("""
            SELECT ae.event_id, e.name, u.username
            FROM assigned_event ae
            JOIN events e ON ae.event_id = e.eventID
            JOIN friends f 
                ON ((f.user_id = %s AND f.friend_id = ae.user_id) 
                    OR (f.friend_id = %s AND f.user_id = ae.user_id))
            JOIN users u ON u.user_id = ae.user_id
            WHERE f.status = 'accepted'
              AND ae.user_id != %s
        """, (user_id, user_id, user_id))
        return self.cursor.fetchall()


