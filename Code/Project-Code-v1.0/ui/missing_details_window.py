import tkinter as tk
from ui.utils import center_window

class MissingDetailsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Μη Επαρκή Στοιχεία")
        self.config(bg="#22A298")
        center_window(self, 400, 200)

        label = tk.Label(self, text="Μη επαρκή στοιχεία για το event!\nΣυμπλήρωσε όλα τα πεδία για να συνεχίσεις.",
                         font=("Arial", 12), bg="#22A298", fg="black")
        label.pack(pady=40)

        btn = tk.Button(self, text="Επιστροφή", bg="black", fg="#DDB0B0", font=("Arial", 10, "bold"), command=self.destroy)
        btn.pack(pady=10)
