import tkinter as tk
from tkinter import messagebox

class DataScreen:
    def __init__(self, root, database):
        self.root = root
        self.db = database
        self.profile_data = self.db.fetch_profile_data()

        self.build_ui()

    def build_ui(self):
          
        self.root.geometry("900x700")
         
         
        self.root.resizable(False, False)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

         
        self.bg_canvas = tk.Canvas(self.root, width=screen_width, height=screen_height, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

         
        steps = 100
        for i in range(steps):
            r1, g1, b1 = self.root.winfo_rgb("#22A298")
            r2, g2, b2 = self.root.winfo_rgb("#FFC0CB")
            r = int(r1 + (r2 - r1) * i / steps) // 256
            g = int(g1 + (g2 - g1) * i / steps) // 256
            b = int(b1 + (b2 - b1) * i / steps) // 256
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.bg_canvas.create_rectangle(
                0, i * screen_height // steps, screen_width, (i + 1) * screen_height // steps,
                outline="", fill=color
            )
        self.root.configure(bg="#22A298")

         
        self.frame = tk.Frame(self.root, bg="white")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

         
        tk.Label(self.frame, text="Name:").pack()
        self.name_entry = tk.Entry(self.frame)
        self.name_entry.pack()
        self.name_entry.insert(0, self.profile_data.name)

         
        tk.Label(self.frame, text="Email:").pack()
        self.email_entry = tk.Entry(self.frame)
        self.email_entry.pack()
        self.email_entry.insert(0, self.profile_data.email)

         
        tk.Label(self.frame, text="Phone:").pack()
        self.phone_entry = tk.Entry(self.frame)
        self.phone_entry.pack()
        self.phone_entry.insert(0, self.profile_data.phone_number)

         
        tk.Label(self.frame, text="Address:").pack()
        self.address_entry = tk.Entry(self.frame)
        self.address_entry.pack()
        self.address_entry.insert(0, self.profile_data.address)

         
        tk.Label(self.frame, text="Bio:").pack()
        self.bio_text = tk.Text(self.frame, height=5)
        self.bio_text.pack()
        self.bio_text.insert("1.0", self.profile_data.bio)

      

         
        save_btn = tk.Button(self.frame, text="Save", bg="#22A298", fg="white", command=self.save_data)
        save_btn.pack(pady=10)

         
        cancel_btn = tk.Button(self.frame, text="Cancel", bg="gray", fg="white", command=self.cancel_edit)
        cancel_btn.pack()

    def save_data(self):
         
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        bio = self.bio_text.get("1.0", "end").strip()

         
        if not all([name, email, phone, address, bio]):
            messagebox.showerror("Error", "Κάποια πεδία του προφίλ είναι κενά!")
            return

        if not phone:
            messagebox.showerror("Error", "Phone number is a required field!")
            return

         
        self.profile_data.name = name
        self.profile_data.email = email
        self.profile_data.phone_number = phone
        self.profile_data.address = address
        self.profile_data.bio = bio

        try:
             
            self.db.update_profile(self.profile_data)
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.go_back_to_profile()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update profile: {str(e)}")

    def cancel_edit(self):
        if messagebox.askyesno("Cancel", "Are you sure you want to cancel? Unsaved changes will be lost."):
            self.go_back_to_profile()

    def go_back_to_profile(self):
        for widget in self.root.winfo_children():
            widget.destroy()
         
        from ui.profile_screen import ProfileScreen
        ProfileScreen(self.root, self.db)

