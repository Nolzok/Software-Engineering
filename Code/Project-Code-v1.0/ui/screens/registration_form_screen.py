import tkinter as tk
from tkinter import messagebox
from models.participation_form import ParticipationForm  # Fixed import
from models.database import Database  # Add this import
from screens.warning_window import WarningWindow
from screens.complete_participation_screen import CompleteParticipationScreen
from screens.timeout import TimeOut
import threading

class RegistrationFormScreen:
    def __init__(self, root, timeout_callback, event_id):
        self.form = ParticipationForm(seat_number=1, event_id=event_id)
        self.db = Database()
        self.timeout_callback = timeout_callback
        self.event_id = event_id
        
        self.root = root
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.frame = tk.Frame(self.root, bg="#FFFFFF", bd=2, relief="ridge")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.entries = {}
        self.create_form()
        
        # Start timeout timer
        self.timer = threading.Timer(30.0, self.handle_timeout)
        self.timer.start()

    def create_form(self):
        fields = [
            "Ονοματεπώνυμο", "Ηλικία", "Τηλέφωνο", "Email",
            "Ενδιαφέροντα/Προτιμήσεις",
            "Διατροφικές προτιμήσεις/αλλεργίες",
            "Ειδικές ανάγκες ή αιτήματα"
        ]

        for field in fields:
            frame = tk.Frame(self.frame, bg="#FFFFFF")
            frame.pack(fill="x", pady=5)
            tk.Label(frame, text=field, bg="#FFFFFF", 
                    font=("Helvetica", 12)).pack(anchor="w")
            entry = tk.Entry(frame, bg="#f0f0f0", relief="flat", 
                           font=("Helvetica", 12))
            entry.pack(fill="x")
            self.entries[field] = entry

        # Create button frame
        button_frame = tk.Frame(self.frame, bg="#FFFFFF")
        button_frame.pack(fill="x", pady=10)
        
        # Back button
        tk.Button(button_frame, 
             text="Πίσω", 
             command=self.go_back,
             font=("Helvetica", 14, "bold"), 
             bg="#a23535", 
             fg="white", 
             bd=0, 
             relief="flat", 
             padx=10, 
             pady=5).pack(side=tk.LEFT, padx=10)
                 
        # Submit button (moved to button frame)
        tk.Button(button_frame, 
                 text="Υποβολή", 
                 command=self.submit_form,
                 font=("Helvetica", 14, "bold"), 
                 bg="#1f96d2", 
                 fg="white", 
                 bd=0, 
                 relief="flat", 
                 padx=10, 
                 pady=5).pack(side=tk.RIGHT, padx=10)

    def handle_timeout(self):
        self.db.release_seat(1)  # Release the temporarily booked seat
        TimeOut().display()  # This will now show the popup
        self.frame.destroy()
        from screens.search import EventApp
        EventApp(self.root)

    def submit_form(self):
        if self.timer:
            self.timer.cancel()
            
        # Map form fields to database fields
        field_mapping = {
            "Ονοματεπώνυμο": "full_name",
            "Ηλικία": "age",
            "Τηλέφωνο": "phone_number",
            "Email": "email",
            "Ενδιαφέροντα/Προτιμήσεις": "interests",
            "Διατροφικές προτιμήσεις/αλλεργίες": "dietary_preferences",
            "Ειδικές ανάγκες ή αιτήματα": "special_needs"
        }
        
        form_data = {field_mapping[field]: entry.get() 
                    for field, entry in self.entries.items()}
        
        # Check all required fields first
        if not all(form_data.values()):
            WarningWindow().display("Insufficient data! Fill in all fields to continue")
            return
            
        # Only validate age format if all fields are filled
        try:
            age = int(form_data['age'])
            if age <= 0 or age > 120:
                WarningWindow().display("Η ηλικία πρέπει να είναι μεταξύ 1 και 120!")
                return
        except ValueError:
            WarningWindow().display("Η ηλικία πρέπει να είναι αριθμός!")
            return

        # Update form object with collected data
        for field, value in form_data.items():
            setattr(self.form, field, value)
            
        # Save to database
        if self.db.save_data(self.form):
            CompleteParticipationScreen().display()
            self.root.destroy()  # Close form window
        else:
            WarningWindow().display("Error saving to database")

    def complete_participation(self):
        self.form.complete_participation()
        CompleteParticipationScreen().display()

    def time_out_message(self):
        TimeOut().display()

    def cleanup(self):
        if self.timer:
            self.timer.cancel()

    def go_back(self):
        if self.timer:
            self.timer.cancel()
        self.frame.destroy()
        from screens.search import EventApp
        EventApp(self.root)
