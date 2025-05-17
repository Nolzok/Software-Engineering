import tkinter as tk
from tkinter import messagebox
from ui.utils import center_window


def show_category_screen(root, controller, category):
    screen = tk.Toplevel(root)
    screen.title("Επιλογή Ανταμοιβής")
    screen.geometry("600x500")
    center_window(screen)    
    screen.config(bg="#22A298")

    # Top bar
    top_frame = tk.Frame(screen, bg="#166A64")
    top_frame.pack(fill=tk.X, pady=5)

    tk.Label(top_frame, text=f"Κατηγορία: {category}", font=("Arial", 14, "bold"),
             bg="#166A64", fg="white").pack(side=tk.LEFT, padx=10)

   
    tk.Label(screen, text="Επέλεξε Ανταμοιβή", font=("Arial", 14, "bold"),
             bg="#22A298", fg="black").pack(pady=20)

    # Συνάρτηση εξαργύρωσης
    def redeem(option):
        if option not in ["Προσφορά", "Κουπόνι"]:
            messagebox.showerror("Μη έγκυρη επιλογή", "Επιλέξτε έγκυρη ανταμοιβή.")
            return

        if controller.client.points_system.deduct_points(50):
            redemption = controller.create_redemption(category, option)
            redemption.redeem_points()
            messagebox.showinfo("Επιτυχία", "Η εξαργύρωση ολοκληρώθηκε.")
            screen.destroy()
        else:
            messagebox.showerror("Αποτυχία", "Δεν υπάρχουν αρκετοί πόντοι.")

    # Κουμπιά επιλογών
    tk.Button(screen, text="Προσφορά", font=("Arial", 12, "bold"),
              bg="black", fg="#DDB0B0", width=25,
              command=lambda: redeem("Προσφορά")).pack(pady=10)

    tk.Button(screen, text="Κουπόνι", font=("Arial", 12, "bold"),
              bg="black", fg="#DDB0B0", width=25,
              command=lambda: redeem("Κουπόνι")).pack(pady=10)
