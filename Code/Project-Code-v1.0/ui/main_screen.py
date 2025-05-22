import tkinter as tk
from ui.profile_ui import ProfileUI

class MainScreen:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Unignite - Main Screen")
        self.root.geometry("800x500")
        self.root.configure(bg="#F5F5F5")

        label = tk.Label(self.root, text="Καλώς ήρθες στην Unignite!", font=("Helvetica", 20, "bold"), bg="#F5F5F5")
        label.pack(pady=40)

        profile_btn = tk.Button(self.root, text="Προφίλ", font=("Helvetica", 14),
                                bg="#22A298", fg="white", padx=20, pady=10,
                                command=self.open_profile)
        profile_btn.pack(pady=10)

        exit_btn = tk.Button(self.root, text="Έξοδος", font=("Helvetica", 14),
                             bg="gray", fg="white", padx=20, pady=10,
                             command=self.root.quit)
        exit_btn.pack(pady=10)

    def open_profile(self):
        ProfileUI(self.root)
