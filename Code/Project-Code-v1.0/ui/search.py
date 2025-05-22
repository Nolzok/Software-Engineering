import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
from models.database import Database
from screens.registration_form_screen import RegistrationFormScreen
from datetime import datetime
import tkinter as tk
from tkinter import font
import subprocess
import os


class EventApp:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.root.title("Αναζήτηση Εκδηλώσεων")
        self.root.geometry("700x600")
        self.root.config(bg="#22A298")

        top_frame = tk.Frame(root, bg="#166A64")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(top_frame, textvariable=self.search_var, font=("Arial", 14))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        search_btn = tk.Button(top_frame, text="Αναζήτηση",
                               font=("Arial", 12, "bold"),
                               bg="black", fg="#DDB0B0",
                               activebackground="#166A64",
                               command=self.search_keywords)
        search_btn.pack(side=tk.LEFT, padx=5)

        filter_btn = tk.Button(top_frame, text="Φίλτρα",
                               font=("Arial", 12, "bold"),
                               bg="black", fg="#DDB0B0",
                               activebackground="#166A64",
                               command=self.show_filters)
        filter_btn.pack(side=tk.LEFT, padx=5)

        self.results_frame = tk.Frame(root, bg="#22A298")
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.category_buttons = []

    def get_events(self):
        events = self.db.get_events()
        return events

    def search_keywords(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        keyword = self.search_var.get().strip().lower()
        events = self.get_events()

        filtered_events = []
        for e in events:
            name_lower = e["name"].lower()
            details_lower = (e.get("details") or "").lower() + e["location"].lower()
            if keyword == "" or keyword in name_lower or keyword in details_lower:
                filtered_events.append(e)

        if not filtered_events:
            label = tk.Label(self.results_frame, text="Δεν βρέθηκαν αποτελέσματα.",
                             font=("Arial", 14, "bold"), fg="white", bg="#22A298")
            label.pack(pady=20)
            return

        categories = {}
        for e in filtered_events:
            cat = e["category"].capitalize()
            categories.setdefault(cat, []).append(e)

        for cat, events_list in categories.items():
            btn = tk.Button(self.results_frame, text=f"{cat} ({len(events_list)})",
                            font=("Arial", 12, "bold"),
                            bg="black", fg="#DDB0B0",
                            activebackground="#166A64",
                            width=30,
                            command=lambda c=cat, ev=events_list: self.show_category_events(c, ev))
            btn.pack(pady=5)
            self.category_buttons.append(btn)

    def show_category_events(self, category, events_list):
        win = tk.Toplevel(self.root)
        win.title(f"Εκδηλώσεις: {category}")
        win.geometry("500x400")
        win.configure(bg="#22A298")

        label = tk.Label(win, text=f"Εκδηλώσεις Κατηγορίας: {category}",
                         font=("Arial", 14, "bold"), bg="#166A64", fg="white")
        label.pack(fill=tk.X, pady=10)

        frame = tk.Frame(win, bg="#22A298")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, font=("Arial", 12),
                             bg="white", fg="#166A64", selectbackground="#1C817A")
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for event in events_list:
            listbox.insert(tk.END, event["name"])

        scrollbar.config(command=listbox.yview)

        def on_select(evt):
            w = evt.widget
            if not w.curselection():
                return
            index = int(w.curselection()[0])
            event = events_list[index]
            self.show_event_details(event)

        listbox.bind('<<ListboxSelect>>', on_select)

    def show_event_details(self, event):
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Λεπτομέρειες Εκδήλωσης")
        detail_window.geometry("700x600")
        detail_window.configure(bg="#22A298")

        # Δημιουργία custom font με μεγαλύτερο μέγεθος και υπογράμμιση για τους τίτλους
        title_font = font.Font(family="Helvetica", size=14, underline=1)
        title_color = "#DDB0B0"  # Ροζ χρώμα (Hot Pink)

        # Δημιουργία font για το περιεχόμενο με λίγο μεγαλύτερο μέγεθος χωρίς υπογράμμιση
        content_font = font.Font(family="Helvetica", size=12)

        # Εμφάνιση πεδίων με ροζ, υπογραμμισμένα τα labels και μεγαλύτερα γράμματα
        tk.Label(detail_window, text="Τίτλος:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10)
        tk.Label(detail_window, text=event['name'], font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20)

        tk.Label(detail_window, text="Τοποθεσία:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10)
        tk.Label(detail_window, text=event['location'], font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20)

        tk.Label(detail_window, text="Ημερομηνία/Ώρα:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10)
        tk.Label(detail_window, text=event['datetime'], font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20)

        tk.Label(detail_window, text="Κατηγορία:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10)
        tk.Label(detail_window, text=event['category'], font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20)

        tk.Label(detail_window, text="Τιμή:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10)
        tk.Label(detail_window, text=f"{event['price']}€", font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20)

        tk.Label(detail_window, text="Διάρκεια:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10)
        tk.Label(detail_window, text=f"{event['duration']} λεπτά", font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20)

        tk.Label(detail_window, text="Μέγιστοι Συμμετέχοντες:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10)
        tk.Label(detail_window, text=event['maxParticipants'], font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20)

        tk.Label(detail_window, text="Περιγραφή:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10, pady=(10,0))
        tk.Message(detail_window, text=event['details'], width=400, font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20, pady=5)

        # Κουμπί για τη φόρμα συμμετοχής
        participation_btn = tk.Button(
            detail_window,
            text="Δήλωση Ενδιαφέροντος",
            font=("Arial", 12, "bold"),
            bg="black", fg="#DDB0B0", activebackground="#166A64",
            command=lambda e=event: self.open_registration_form(e['id'])  # <-- fix here
        )
        participation_btn.pack(pady=15)

        # Get seat availability from the database
        seats_info = self.db.get_event_seats(event['id'])

        tk.Label(detail_window, text="Διαθεσιμότητα Θέσεων:", font=title_font, fg=title_color, bg="#22A298").pack(anchor="w", padx=10)
        tk.Label(detail_window, text=f"{seats_info['available']} διαθέσιμες από {seats_info['total']}", font=content_font, fg="white", bg="#22A298").pack(anchor="w", padx=20)

    def show_filters(self):
        win = tk.Toplevel(self.root)
        win.title("Φίλτρα")
        win.geometry("300x150")
        win.configure(bg="#22A298")

        label = tk.Label(win, text="Επίλεξε φίλτρο:", font=("Arial", 14, "bold"),
                         bg="#22A298", fg="white")
        label.pack(pady=10)

        def apply_filter_date():
            self.apply_filter("Ημερομηνία")
            win.destroy()

        def apply_filter_price():
            self.apply_filter("Τιμή")
            win.destroy()

        btn1 = tk.Button(win, text="Ημερομηνία",
                         font=("Arial", 12, "bold"),
                         bg="black", fg="#DDB0B0",
                         activebackground="#166A64",
                         width=20, command=apply_filter_date)
        btn1.pack(pady=5)

        btn2 = tk.Button(win, text="Τιμή",
                         font=("Arial", 12, "bold"),
                         bg="black", fg="#DDB0B0",
                         activebackground="#166A64",
                         width=20, command=apply_filter_price)
        btn2.pack(pady=5)

    def apply_filter(self, filter_name):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        events = self.get_events()

        def parse_datetime(dt_str):
            try:
                return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            except Exception:
                return datetime.max

        if filter_name == "Ημερομηνία":
            filtered = sorted(events, key=lambda e: parse_datetime(e.get("datetime", "")))
        elif filter_name == "Τιμή":
            filtered = sorted(events, key=lambda e: e.get("price", 0))
        else:
            filtered = events

        if not filtered:
            label = tk.Label(self.results_frame, text="Δεν βρέθηκαν events με το φίλτρο.",
                             font=("Arial", 14, "bold"), fg="white", bg="#22A298")
            label.pack(pady=20)
            return

        for event in filtered:
            btn = tk.Button(self.results_frame,
                            text=f"{event['name']} - {event['datetime']} - {event['price']}€",
                            font=("Arial", 12),
                            anchor="w",
                            bg="black", fg="#DDB0B0",
                            activebackground="#166A64",
                            command=lambda ev=event: self.show_event_details(ev))
            btn.pack(fill=tk.X, pady=2, padx=5)

    def open_registration_form(self, event_id):
        RegistrationFormScreen(self.root, timeout_callback=None, event_id=event_id)


if __name__ == "__main__":
    root = tk.Tk()
    app = EventApp(root)
    root.mainloop()