import tkinter as tk
from tkinter import messagebox
from ui.events_screen import EventsScreen
from models.event import Event  


class SummaryScreen(tk.Toplevel):
    def __init__(self, master, event_data: Event, organizer):
        super().__init__(master)
        self.event = event_data  
        self.organizer = organizer
        self.title("Σύνοψη Event")

        self.configure(bg="#22A298")
        self.geometry("600x450")

        self.build_ui()

    def build_ui(self):
        label = tk.Label(self, text="Επιβεβαίωση Event", font=("Arial", 16, "bold"), bg="#22A298", fg="black")
        label.pack(pady=20)

        summary_text = (
            f"Όνομα: {self.event.name}\n"
            f"Τοποθεσία: {self.event.location}\n"
            f"Ημερομηνία & Ώρα: {self.event.date.strftime('%d/%m/%Y %H:%M')}\n"
            f"Κατηγορία: {self.event.category}\n"
            f"Διάρκεια: {self.event.duration}\n"
            f"Περιγραφή: {self.event.description}\n"
            f"Τιμή: {self.event.price}\n"
            f"Μέγιστος αριθμός συμμετεχόντων: {self.event.max_participants}"
        )

        summary_label = tk.Label(self, text=summary_text, justify="left",
                                 bg="#DDB0B0", fg="black", font=("Arial", 12), padx=20, pady=15, relief="ridge")
        summary_label.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        button_frame = tk.Frame(self, bg="#22A298")
        button_frame.pack(pady=20)

        cancel_btn = tk.Button(button_frame, text="Ακύρωση", font=("Arial", 12, "bold"),
                               bg="#166A64", fg="white", width=12, command=self.cancel_event)
        cancel_btn.grid(row=0, column=0, padx=15)

        submit_btn = tk.Button(button_frame, text="Οριστική Δημιουργία", font=("Arial", 12, "bold"),
                               bg="#166A64", fg="white", width=16, command=self.submit_event)
        submit_btn.grid(row=0, column=1, padx=15)

    def cancel_event(self):
        self.destroy()
        self.master.destroy()
        events_screen = EventsScreen(self.organizer)
        events_screen.mainloop()

    def submit_event(self):
        success = self.organizer.submit_event(self.event)
        if success:
            messagebox.showinfo("Επιτυχία", "Το Event δημιουργήθηκε επιτυχώς!")
            self.destroy()
            self.master.destroy()
            from ui.events_screen import EventsScreen
            events_screen = EventsScreen(self.organizer)
            events_screen.mainloop()
        else:
            messagebox.showerror("Σφάλμα", "Δεν ήταν δυνατή η αποθήκευση του event.")
