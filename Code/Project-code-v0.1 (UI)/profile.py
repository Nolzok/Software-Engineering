import tkinter as tk
from tkinter import messagebox

def show_profile_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
    
    root.title("Unignite")
    root.geometry("800x500")
    root.configure(bg="#F5F5F5")

    # Sidebar
    sidebar = tk.Frame(root, bg="#1E8A7A", width=200)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    logo = tk.Label(sidebar, text="Unignite", font=("Helvetica", 18, "bold"), bg="#1E8A7A", fg="white")
    logo.pack(pady=20)

    # Gradient background
    GRADIENT_TOP = "#22A298"
    GRADIENT_BOTTOM = "#FFC0CB"

    content_frame = tk.Frame(root, bg="#F5F5F5")
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(content_frame, width=600, height=500)
    canvas.pack(fill=tk.BOTH, expand=True)

    for i in range(500):
        r1, g1, b1 = root.winfo_rgb(GRADIENT_TOP)
        r2, g2, b2 = root.winfo_rgb(GRADIENT_BOTTOM)
        r = int(r1 + (r2 - r1) * i / 500)
        g = int(g1 + (g2 - g1) * i / 500)
        b = int(b1 + (b2 - b1) * i / 500)
        color = f"#{r // 256:02x}{g // 256:02x}{b // 256:02x}"
        canvas.create_line(0, i, 600, i, fill=color)

    # Profile content
    profile_label = tk.Label(content_frame, text="Profile", font=("Helvetica", 20, "bold"), bg="#F5F5F5")
    profile_label.place(x=20, y=20)

    info_frame = tk.Frame(content_frame, bg="#F5F5F5")
    info_frame.place(x=20, y=70)

    # Profile information
    tk.Label(info_frame, text="Username: Bill", bg="#F5F5F5", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w", pady=(10, 0))
    tk.Label(info_frame, text="Friend Code: FC123456", bg="#F5F5F5", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
    tk.Label(info_frame, text="Friends: 42", bg="#F5F5F5", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")

    tk.Label(info_frame, text="Bio:", bg="#F5F5F5", font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="w", pady=(20, 0))
    bio_display = tk.Text(info_frame, height=5, width=60, font=("Helvetica", 11))
    bio_display.grid(row=5, column=0, sticky="w")
    bio_display.insert("1.0", "Hello, this is my profile!")
    bio_display.config(state=tk.DISABLED)

    # Buttons
    btn_frame = tk.Frame(info_frame, bg="#F5F5F5")
    btn_frame.grid(row=6, column=0, pady=20, sticky="w")

    modify_btn = tk.Button(btn_frame, text="Modify Data",
                          command=lambda: show_edit_window(root, bio_display),
                          bg="#22A298", fg="white", font=("Helvetica", 11, "bold"),
                          padx=10, pady=5)
    modify_btn.grid(row=0, column=0, padx=5)

def show_edit_window(root, bio_display):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Profile")
    edit_window.geometry("400x250")
    edit_window.configure(bg="#F5F5F5")

    tk.Label(edit_window, text="Edit Bio:", font=("Helvetica", 12, "bold"), bg="#F5F5F5").pack(pady=10)
    bio_input = tk.Text(edit_window, height=5, width=45, font=("Helvetica", 11))
    bio_input.pack()
    bio_input.insert("1.0", bio_display.get("1.0", "end-1c"))

    btn_frame = tk.Frame(edit_window, bg="#F5F5F5")
    btn_frame.pack(pady=20)

    def save_bio():
        new_bio = bio_input.get("1.0", "end").strip()
        if new_bio:
            bio_display.config(state=tk.NORMAL)
            bio_display.delete("1.0", "end")
            bio_display.insert("1.0", new_bio)
            bio_display.config(state=tk.DISABLED)
            edit_window.destroy()
        else:
            messagebox.showwarning("Warning", "Bio cannot be empty!")

    tk.Button(btn_frame, text="Save", command=save_bio,
              bg="#22A298", fg="white").grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Exit", command=edit_window.destroy,
              bg="gray", fg="white").grid(row=0, column=1, padx=10)

def main():
    root = tk.Tk()
    root.title("Unignite - Main Screen")
    root.geometry("800x500")
    root.configure(bg="#F5F5F5")
    
    tk.Button(root, text="Select Profile Icon", 
              command=lambda: show_profile_screen(root),
              bg="#22A298", fg="white").pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    main()
