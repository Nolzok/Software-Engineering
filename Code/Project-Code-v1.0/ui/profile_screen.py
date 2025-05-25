import tkinter as tk
from tkinter import messagebox
from ui.data_screen import DataScreen   

class ProfileScreen:
    def __init__(self, root, database):
        self.root = root
        self.db = database
        self.profile_data = self.db.fetch_profile_data()
        self.build_ui()

    def build_ui(self):
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        screen_width = 900
        screen_height = 700

         
        self.bg_canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        steps = 200
        r1, g1, b1 = self.root.winfo_rgb("#22A298")
        r2, g2, b2 = self.root.winfo_rgb("#FFC0CB")
        for i in range(steps):
            r = int(r1 + (r2 - r1) * i / steps) // 256
            g = int(g1 + (g2 - g1) * i / steps) // 256
            b = int(b1 + (b2 - b1) * i / steps) // 256
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = int(i * screen_height / steps)
            y2 = int((i + 1) * screen_height / steps)
            self.bg_canvas.create_rectangle(0, y1, screen_width, y2, outline="", fill=color)

         
        sidebar = tk.Frame(self.root, bg="#133F3F", width=200)
        sidebar.place(x=0, y=0, width=200, height=700)
        sidebar.pack_propagate(False)
        tk.Label(sidebar,
                 text="Menu",
                 font=("Arial", 16, "bold"),
                 bg="#133F3F",
                 fg="white").pack(pady=(10,20))

        def do_nothing():
            pass

        def open_profile():
            profile_window = tk.Toplevel(self.root)
            ProfileScreen(profile_window, self.db)

        for text, cmd in [
            ("Σύστημα Επιβράβευσης", do_nothing),
            ("Προφίλ", open_profile),
            ("Κριτικές-Αξιολογήσεις", do_nothing),
            ("Δωρεές", do_nothing),
            ("Πρόσκληση Φίλων", do_nothing),
            ("Χαμένα Αντικείμενα", do_nothing),
            ("Ειδοποιήσεις", do_nothing)
        ]:
            tk.Button(sidebar,
                      text=text,
                      font=("Times", 14),
                      bg="#DDB0B0",
                      fg="black",
                      width=20,
                      command=cmd).pack(pady=5)

         
        content_frame = tk.Frame(self.root, bg="white", padx=20, pady=20)
        content_frame.place(x=210, y=30, width=670, height=640)

        tk.Label(content_frame, text="Your Profile", font=("Arial", 20), fg="#22A298", bg="white").pack(pady=10)

        if self.missing_data():
            messagebox.showerror("Error", "Κάποια πεδία του προφίλ είναι κενά!")
            return

        label_kwargs = {"fg": "#333333", "font": ("Arial", 12), "bg": "white"}

        tk.Label(content_frame, text=f"Name: {self.profile_data.name}", **label_kwargs).pack(anchor="w", pady=3)
        tk.Label(content_frame, text=f"Email: {self.profile_data.email}", **label_kwargs).pack(anchor="w", pady=3)
        tk.Label(content_frame, text=f"Phone: {self.profile_data.phone_number}", **label_kwargs).pack(anchor="w", pady=3)
        tk.Label(content_frame, text=f"Address: {self.profile_data.address}", **label_kwargs).pack(anchor="w", pady=3)
        tk.Label(content_frame, text=f"Bio: {self.profile_data.bio}", **label_kwargs).pack(anchor="w", pady=3)
        tk.Label(content_frame, text=f"Friend Code: {self.profile_data.friendCode}", fg="#22A298", bg="white", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(content_frame, text=f"Friends: {self.profile_data.friends}", **label_kwargs).pack(anchor="w", pady=3)

        tk.Button(
            content_frame,
            text="Edit Profile",
            command=self.open_data_screen,
            bg="#22A298", fg="white",
            font=("Arial", 12, "bold"),
            padx=20, pady=8,
            activebackground="#1E7E70", activeforeground="white"
        ).pack(pady=20)

         
        self.root.bind("<Escape>", lambda e: self.root.destroy())

    def missing_data(self):
        return any([
            not self.profile_data.name,
            not self.profile_data.email,
            not self.profile_data.phone_number,
            not self.profile_data.address,
            not self.profile_data.bio
        ])

    def open_data_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        DataScreen(self.root, self.db)
