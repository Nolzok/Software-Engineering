import tkinter as tk
from tkinter import messagebox
from models.partitipation_form import ParticipationForm   
from database.database import Database_2   

from ui.warning_window import WarningWindow
from ui.complete_participation_screen import CompleteParticipationScreen
from ui.timeout import TimeOut
import threading

class RegistrationFormScreen:
    def __init__(self, root, timeout_callback, event_id):
        self.form = ParticipationForm(seat_number=1, event_id=event_id)
        self.db = Database_2()
        self.timeout_callback = timeout_callback
        self.event_id = event_id
        
        self.root = root
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.frame = tk.Frame(self.root, bg="#FFFFFF", bd=2, relief="ridge")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.entries = {}
        self.create_form()
        
         
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

         
        button_frame = tk.Frame(self.frame, bg="#FFFFFF")
        button_frame.pack(fill="x", pady=10)
        
         
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
        self.db.release_seat(1)   
        TimeOut().display()   
        self.frame.destroy()
        from ui.search import EventApp
        EventApp(self.root)

    def submit_form(self):
        if self.timer:
            self.timer.cancel()
            
         
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
        
         
        if not all(form_data.values()):
            WarningWindow().display("Insufficient data! Fill in all fields to continue")
            return
            
         
        try:
            age = int(form_data['age'])
            if age <= 0 or age > 120:
                WarningWindow().display("Η ηλικία πρέπει να είναι μεταξύ 1 και 120!")
                return
        except ValueError:
            WarningWindow().display("Η ηλικία πρέπει να είναι αριθμός!")
            return

         
        for field, value in form_data.items():
            setattr(self.form, field, value)
            
         
        if self.db.save_data(self.form):
            CompleteParticipationScreen().display()
            self.root.destroy()   
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
        from ui.search import EventApp
        EventApp(self.root)
