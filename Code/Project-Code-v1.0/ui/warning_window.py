import tkinter as tk
from tkinter import messagebox

class WarningWindow:
    def __init__(self, root, message="Λείπουν υποχρεωτικά πεδία!", on_ok=None):
        self.window = tk.Toplevel(root)
        self.window.title("Προειδοποίηση")
        self.window.geometry("300x150")
        self.window.configure(bg="#FFE4E1")

        label = tk.Label(self.window, text=message, font=("Helvetica", 12), bg="#FFE4E1", fg="red", wraplength=250)
        label.pack(pady=20)

        def ok_and_callback():
            self.window.destroy()
            if on_ok:
                on_ok()

        close_btn = tk.Button(self.window, text="OK", command=ok_and_callback, bg="#D9534F", fg="white")
        close_btn.pack(pady=10)


