import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import simpledialog
from models.notifications import Notifications_System   

class NotificationsScreen(tk.Frame):
    def __init__(self, parent, notification_system, current_user):
        super().__init__(parent, bg="#22A298")        
        self.ns = notification_system
        self.current_user = current_user
        self.mute_var = tk.BooleanVar(value=self.ns.notifications_muted)  

    def show(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Settings button instead of mute checkbox
        settings_frame = tk.Frame(self, bg="#22A298")
        settings_frame.pack(anchor="ne", padx=10, pady=10)

        settings_button = tk.Button(
            settings_frame,
            text="Settings ⚙️",
            command=self.notifications_settings_subscreen,
            bg="#ffffff",
            fg="#000000"
        )
        settings_button.pack()

        # Notification display
        notifications = self.ns.get_notifications(self.current_user)
        if not notifications:
            tk.Label(self, text="No new notifications.", font=("Helvetica", 18), bg="white").pack(pady=50)
            return

        tk.Label(self, text="Event Notifications:", font=("Helvetica", 18), bg="white").pack(pady=10)

        for event_id, event_name, username in notifications:
            msg = f"{username} added to event '{event_name}' (Event ID: {event_id})"
            tk.Label(self, text=msg, font=("Helvetica", 14), bg="white").pack(anchor='w', padx=10, pady=5)

    def notifications_settings_subscreen(self):
        popup = tk.Toplevel(self)
        popup.title("Notification Settings")
        popup.configure(bg="#f0f0f0")
        popup.geometry("300x150")
        popup.grab_set()  # Makes the popup modal

        mute_checkbox = tk.Checkbutton(
            popup,
            text="Mute Notifications",
            variable=self.mute_var,
            bg="#f0f0f0",
            command=self.toggle_mute
        )
        mute_checkbox.pack(pady=20)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack()

    def toggle_mute(self):
     self.ns.notifications_muted = self.mute_var.get()
     self.show()  # Refresh the screen immediately
