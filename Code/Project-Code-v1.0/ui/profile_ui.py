import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
from models.profile import Profile


class ProfileUI:
    def __init__(self, root, profile_data=None):
        self.root = root
        self.root.title("Unignite")
        self.root.geometry("800x500")
        self.root.configure(bg="#F5F5F5")

        self.profile_data = profile_data or Profile("Bill", "bill@example.com", "1234567890", "Athens", "Hello, this is my profile!")

        self.show_profile_screen()
        

    def show_profile_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        sidebar = tk.Frame(self.root, bg="#1E8A7A", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        logo = tk.Label(sidebar, text="Unignite", font=("Helvetica", 18, "bold"), bg="#1E8A7A", fg="white")
        logo.pack(pady=20)

        GRADIENT_TOP = "#22A298"
        GRADIENT_BOTTOM = "#FFC0CB"

        content_frame = tk.Frame(self.root, bg="#F5F5F5")
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(content_frame, width=600, height=500)
        canvas.pack(fill=tk.BOTH, expand=True)

        for i in range(500):
            r1, g1, b1 = self.root.winfo_rgb(GRADIENT_TOP)
            r2, g2, b2 = self.root.winfo_rgb(GRADIENT_BOTTOM)
            r = int(r1 + (r2 - r1) * i / 500)
            g = int(g1 + (g2 - g1) * i / 500)
            b = int(b1 + (b2 - b1) * i / 500)
            color = f"#{r // 256:02x}{g // 256:02x}{b // 256:02x}"
            canvas.create_line(0, i, 600, i, fill=color)

        profile_label = tk.Label(content_frame, text="Profile", font=("Helvetica", 20, "bold"), bg="#F5F5F5")
        profile_label.place(x=20, y=20)

        info_frame = tk.Frame(content_frame, bg="#F5F5F5")
        info_frame.place(x=20, y=70)

        profile_frame = tk.Frame(info_frame, bg="#F5F5F5")
        profile_frame.grid(row=0, column=0, pady=10, sticky="w")

        self.image_label = tk.Label(profile_frame, bg="#1E8A7A", width=100, height=100)
        self.image_label.pack(side=tk.LEFT, padx=10)

        def update_profile_image():
            new_image = self.select_profile_image()
            if new_image:
                self.profile_data.profile_image = new_image
                self.image_label.config(image=new_image)
                self.image_label.image = new_image

        tk.Button(profile_frame, text="Change Picture",
                  command=update_profile_image,
                  bg="#22A298", fg="white").pack(side=tk.LEFT)

        tk.Label(info_frame, text=f"Username: {self.profile_data.name}", bg="#F5F5F5", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=(10, 0))
        tk.Label(info_frame, text=f"Email: {self.profile_data.email}", bg="#F5F5F5", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
        tk.Label(info_frame, text=f"Phone: {self.profile_data.phoneNumber}", bg="#F5F5F5", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")
        tk.Label(info_frame, text=f"Address: {self.profile_data.address}", bg="#F5F5F5", font=("Helvetica", 12)).grid(row=4, column=0, sticky="w")

        tk.Label(info_frame, text="Bio:", bg="#F5F5F5", font=("Helvetica", 12, "bold")).grid(row=5, column=0, sticky="w", pady=(20, 0))
        self.bio_display = tk.Text(info_frame, height=5, width=60, font=("Helvetica", 11))
        self.bio_display.grid(row=6, column=0, sticky="w")
        self.bio_display.insert("1.0", self.profile_data.bio)
        self.bio_display.config(state=tk.DISABLED)

        btn_frame = tk.Frame(info_frame, bg="#F5F5F5")
        btn_frame.grid(row=7, column=0, pady=20, sticky="w")

        modify_btn = tk.Button(btn_frame, text="Modify Data",
                               command=self.show_edit_window,
                               bg="#22A298", fg="white", font=("Helvetica", 11, "bold"),
                               padx=10, pady=5)
        modify_btn.grid(row=0, column=0, padx=5)

        exit_btn = tk.Button(btn_frame, text="Back",
                             command=self.show_main_screen,
                             bg="gray", fg="white", font=("Helvetica", 11, "bold"),
                             padx=10, pady=5)
        exit_btn.grid(row=0, column=1, padx=5)

    def show_edit_window(self):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Profile")
        edit_window.geometry("400x250")
        edit_window.configure(bg="#F5F5F5")

        tk.Label(edit_window, text="Edit Bio:", font=("Helvetica", 12, "bold"), bg="#F5F5F5").pack(pady=10)
        bio_input = tk.Text(edit_window, height=5, width=45, font=("Helvetica", 11))
        bio_input.pack()
        bio_input.insert("1.0", self.bio_display.get("1.0", "end-1c"))

        btn_frame = tk.Frame(edit_window, bg="#F5F5F5")
        btn_frame.pack(pady=20)

        def on_closing():
            if bio_input.get("1.0", "end").strip() != self.bio_display.get("1.0", "end-1c").strip():
                if messagebox.askokcancel("Exit", "Οι αλλαγές σας δεν θα αποθηκευτούν. Θέλετε να συνεχίσετε;"):
                    edit_window.destroy()
            else:
                edit_window.destroy()

        edit_window.protocol("WM_DELETE_WINDOW", on_closing)

        def save_bio():
            new_bio = bio_input.get("1.0", "end").strip()
            if len(new_bio) > 500:
                messagebox.showwarning("Warning", "Bio must be less than 500 characters")
                return
            if new_bio:
                self.bio_display.config(state=tk.NORMAL)
                self.bio_display.delete("1.0", "end")
                self.bio_display.insert("1.0", new_bio)
                self.bio_display.config(state=tk.DISABLED)
                self.profile_data.bio = new_bio
                edit_window.destroy()
                messagebox.showinfo("Success", "Profile updated successfully!")

        tk.Button(btn_frame, text="Save", command=save_bio,
                  bg="#22A298", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Exit", command=on_closing,
                  bg="gray", fg="white").grid(row=0, column=1, padx=10)

    def show_main_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        label = tk.Label(self.root, text="Main Screen", font=("Helvetica", 20))
        label.pack(pady=20)
        tk.Button(self.root, text="Go to Profile", command=self.show_profile_screen, bg="#22A298", fg="white").pack(pady=10)
