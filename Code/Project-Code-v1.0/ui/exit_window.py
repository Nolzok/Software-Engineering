import tkinter as tk
from tkinter import messagebox

class ExitWindow:
    def __init__(self, root, on_confirm_exit):
        self.window = tk.Toplevel(root)
        self.window.title("Έξοδος Χωρίς Αποθήκευση")
        self.window.geometry("350x160")
        self.window.configure(bg="#FFF8DC")

        label = tk.Label(self.window, text="Οι αλλαγές δεν έχουν αποθηκευτεί.\nΘέλεις να συνεχίσεις;", 
                         font=("Helvetica", 12), bg="#FFF8DC", wraplength=300)
        label.pack(pady=20)

        button_frame = tk.Frame(self.window, bg="#FFF8DC")
        button_frame.pack(pady=10)

        cancel_btn = tk.Button(button_frame, text="Ακύρωση", command=self.window.destroy, bg="gray", fg="white")
        cancel_btn.grid(row=0, column=0, padx=10)

        confirm_btn = tk.Button(button_frame, text="Έξοδος", command=lambda: self.exit_and_close(on_confirm_exit), bg="#D9534F", fg="white")
        confirm_btn.grid(row=0, column=1, padx=10)

    def exit_and_close(self, callback):
        self.window.destroy()
        callback()  # Τρέχει την ενέργεια εξόδου

