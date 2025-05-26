import tkinter as tk
from tkinter import messagebox
from ui.utils import center_window
from ui.summary_screen import SummaryScreen
from ui.missing_details_window import MissingDetailsWindow
from datetime import datetime
from models.event import Event
from db.database import connect_to_mysql  


class FormScreen(tk.Toplevel): 
    def __init__(self, master=None, event_data=None, organizer=None):
        super().__init__(master)
        self.organizer = organizer
        self.event_data = event_data
        self.title("Δημιουργία Event")
        center_window(self, 600, 450)
        self.geometry("600x700")
        self.configure(bg="#22A298")

        title = tk.Label(self, text="Δημιουργία νέου event", font=("Arial", 16, "bold"), bg="#22A298", fg="black")
        title.pack(pady=20)

        labels = [
            "Όνομα", "Τοποθεσία", "Ημερομηνία & Ώρα", "Κατηγορία", "Διάρκεια", "Περιγραφή",
            "Τιμή", "Μέγιστος αριθμός συμμετεχόντων"
        ]

        self.entries = {}

        for label_text in labels:
            label = tk.Label(self, text=label_text, bg="#22A298", fg="black", anchor="w", font=("Arial", 9, "bold"))
            label.pack(fill="x", padx=40, pady=(10, 0))

            if label_text == "Περιγραφή":
                entry = tk.Text(self, bg="#DDB0B0", fg="black", relief="flat", font=("Arial", 15), height=4)
                entry.pack(fill="x", padx=40)
            else:
                entry = tk.Entry(self, bg="#DDB0B0", fg="black", relief="flat", font=("Arial", 15))
                entry.pack(fill="x", padx=40)

            self.entries[label_text] = entry

        submit_button = tk.Button(
            self, text="Αποθήκευση",
            bg="#166A64", fg="white",
            font=("Arial", 15, "bold"),
            command=self.submit_event
        )
        submit_button.pack(pady=30)

    def submit_event(self):
        event_data = {}
        for key, widget in self.entries.items():
            if key == "Περιγραφή":
                value = widget.get("1.0", tk.END).strip()
            else:
                value = widget.get().strip()
            event_data[key] = value

        missing_fields = [field for field, val in event_data.items() if not val]
        if missing_fields:
            MissingDetailsWindow(self)
            return

        try:
            datetime_obj = datetime.strptime(event_data["Ημερομηνία & Ώρα"], "%d/%m/%Y %H:%M")

            event = Event(
                name=event_data["Όνομα"],
                date=datetime_obj,
                location=event_data["Τοποθεσία"],
                max_participants=int(event_data["Μέγιστος αριθμός συμμετεχόντων"]),
                category=event_data["Κατηγορία"],
                price=float(event_data["Τιμή"]),
                duration=int(event_data["Διάρκεια"]),
                description=event_data["Περιγραφή"]
            )
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Λάθος μορφή δεδομένων: {e}")
            return

        self.withdraw()
        summary = SummaryScreen(self, event, organizer=self.organizer)
        summary.grab_set()