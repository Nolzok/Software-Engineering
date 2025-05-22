import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="ioannak25",
                database="unignite"
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Σφάλμα Βάσης", f"Σφάλμα σύνδεσης με τη βάση δεδομένων:\n{err}")
            exit(1)

    def get_lost_items(self):
        self.cursor.execute("SELECT name FROM lost_items")
        results = self.cursor.fetchall()
        return [row['name'] for row in results]

    def get_details(self, item_name):
        self.cursor.execute("SELECT details FROM lost_items WHERE name=%s", (item_name,))
        result = self.cursor.fetchone()
        return result['details'] if result else "Δεν βρέθηκαν λεπτομέρειες."

class LostItemsApp:
    def __init__(self, root):
        self.root = root
        root.title("Χαμένα Αντικείμενα")
        root.geometry("700x600")
        root.configure(bg="#22A298")  # background window

        self.db = Database()

        self.create_main_screen()

    def create_main_screen(self):
        self.clear_root()

        # top frame με background χρώμα από παράδειγμα
        top_frame = tk.Frame(self.root, bg="#166A64")
        top_frame.pack(fill=tk.X, pady=5)

        tk.Label(top_frame, text="Λίστα Χαμένων Αντικειμένων", font=("Arial", 16, "bold"),
                 bg="#166A64", fg="#DDB0B0").pack(side=tk.LEFT, padx=10)

        # λίστα αντικειμένων με ίδιο background με παράδειγμα
        self.listbox = tk.Listbox(self.root, font=("Arial", 14), bg="#22A298", fg="black",
                                  selectbackground="#166A64", selectforeground="white",
                                  highlightthickness=0, relief=tk.FLAT)
        self.listbox.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        try:
            items = self.db.get_lost_items()
            if not items:
                messagebox.showinfo("Μήνυμα", "Δεν υπάρχουν διαθέσιμα χαμένα αντικείμενα.")
            else:
                for item in items:
                    self.listbox.insert(tk.END, item)
        except mysql.connector.Error as err:
            messagebox.showerror("Σφάλμα Βάσης", f"Σφάλμα ανάκτησης δεδομένων:\n{err}")

        # κουμπί με στυλ από το παράδειγμα (μαύρο bg, ρόζ γραμματοσειρά)
        btn_show_details = tk.Button(self.root, text="Δες Λεπτομέρειες",
                                     font=("Arial", 12, "bold"),
                                     bg="black", fg="#DDB0B0",
                                     activebackground="#166A64",
                                     command=self.show_details)
        btn_show_details.pack(pady=5)

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_details(self):
        try:
            selected_index = self.listbox.curselection()[0]
            item_name = self.listbox.get(selected_index)
        except IndexError:
            messagebox.showwarning("Προσοχή", "Επίλεξε πρώτα ένα αντικείμενο.")
            return

        try:
            details = self.db.get_details(item_name)
        except mysql.connector.Error as err:
            messagebox.showerror("Σφάλμα Βάσης", f"Σφάλμα ανάκτησης λεπτομερειών:\n{err}")
            details = "Δεν βρέθηκαν λεπτομέρειες."

        self.clear_root()

        # header με background και font από παράδειγμα
        top_frame = tk.Frame(self.root, bg="#166A64")
        top_frame.pack(fill=tk.X, pady=5)

        tk.Label(top_frame, text=f"Λεπτομέρειες: {item_name}", font=("Arial", 16, "bold"),
                 bg="#166A64", fg="#DDB0B0").pack(side=tk.LEFT, padx=10)

        details_label = tk.Label(self.root, text=details, font=("Arial", 12),
                                 wraplength=350, justify="left",
                                 bg="#22A298", fg="black")
        details_label.pack(pady=10, padx=10)

        btn_identify = tk.Button(self.root, text="Identify",
                                 font=("Arial", 12, "bold"),
                                 bg="black", fg="#DDB0B0",
                                 activebackground="#166A64",
                                 command=lambda: self.ask_phone(item_name))
        btn_identify.pack(pady=5)

        btn_back = tk.Button(self.root, text="Πίσω",
                             font=("Arial", 12, "bold"),
                             bg="black", fg="#DDB0B0",
                             activebackground="#166A64",
                             command=self.create_main_screen)
        btn_back.pack(pady=5)

    def ask_phone(self, item_name):
        phone = simpledialog.askstring("Καταχώρηση Τηλεφώνου", "Εισάγετε το κινητό σας τηλέφωνο:")

        if phone is None:
            return

        phone = phone.strip()
        if self.validate_phone(phone):
            messagebox.showinfo("Επιτυχία", f"Ο αριθμός {phone} καταχωρήθηκε για το αντικείμενο '{item_name}'.")
        else:
            messagebox.showerror("Σφάλμα", "Μη έγκυρος αριθμός! Πρέπει να είναι 10 ψηφία.")

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10


if __name__ == "__main__":
    root = tk.Tk()
    app = LostItemsApp(root)
    root.mainloop()
