from db.database import connect_to_mysql  
import tkinter as tk
from ui.utils import center_window

class EventsScreen(tk.Tk):
    def __init__(self, organizer, form_screen_class=None):
        super().__init__()

        self.organizer = organizer
        self.form_screen_class = form_screen_class
        self.title("Οθόνη με Events διοργανωτή")
        center_window(self, 600, 450)
        self.geometry("500x500")
        self.config(bg="#22A298")

        top_frame = tk.Frame(self, bg="#166A64")
        top_frame.pack(fill=tk.X, pady=5)

        new_event_btn = tk.Button(top_frame, text="Νέο Event", font=("Arial", 10, "bold"), bg="black", fg="#DDB0B0", command=self.open_form)
        new_event_btn.pack(side=tk.RIGHT, padx=10)

        title_frame = tk.Frame(self, bg="black", padx=20, pady=10)
        title_frame.pack(pady=10)

        title_label = tk.Label(title_frame, text="Τα events μου", font=("Arial", 15, "bold"), bg="black", fg="#DDB0B0")
        title_label.pack()

        self.event_listbox = tk.Listbox(self, font=("Arial", 16), height=20, selectbackground="white", activestyle="none", bg="#DDB0B0", fg="black")
        self.event_listbox.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

        self.load_events()

    def load_events(self):
        conn, cursor = connect_to_mysql()
        cursor.execute("""
            SELECT name FROM events
            WHERE organizerID = 4
        """)
        result = cursor.fetchall()
        cursor.close()
        conn.close()

        self.event_listbox.delete(0, tk.END)
        for row in result:
            self.event_listbox.insert(tk.END, row[0])

    def open_form(self):
        self.withdraw()
        new_event = self.organizer.add_event()
        form = self.form_screen_class(master=self, event_data=new_event, organizer=self.organizer)
        form.protocol("WM_DELETE_WINDOW", lambda: self.on_form_close(form))
        form.mainloop()

    def on_form_close(self, form):
        form.destroy()
        self.deiconify()

    def add_event_to_list(self, event_name):
        self.event_listbox.insert(tk.END, event_name)
