import tkinter as tk
from ui.category_screen import show_category_screen
from ui.utils import center_window


def show_categories_screen(root, client):
    categories_window = tk.Toplevel(root)
    categories_window.title("Κατηγορίες Ανταμοιβών")
    categories_window.geometry("600x500")
    center_window(categories_window)
    categories_window.config(bg="#22A298")

    top_frame = tk.Frame(categories_window, bg="#166A64")
    top_frame.pack(fill=tk.X, pady=5)

    tk.Label(top_frame, text="Κατηγορίες Ανταμοιβών", font=("Arial", 14, "bold"),
             bg="#166A64", fg="white").pack(side=tk.LEFT, padx=10)

    tk.Label(categories_window, text="Επίλεξε Κατηγορία", font=("Arial", 14, "bold"),
             bg="#22A298", fg="black").pack(pady=1)

    def on_select(category):
        client.choose_category(root, category)
        categories_window.destroy()

    categories = [
        "Αθλητισμός", "Διασκέδαση", "Τεχνολογία", "Πολιτισμός", "Μουσική",
        "Εκπαίδευση", "Τέχνη", "Επιχειρηματικότητα", "Υγεία & Ευεξία"
    ]

    for category in categories:
        tk.Button(categories_window, text=category, width=25,
                  font=("Arial", 12, "bold"),
                  bg="black", fg="#DDB0B0",
                  command=lambda c=category: on_select(c)).pack(pady=10)
