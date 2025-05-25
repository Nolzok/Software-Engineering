import tkinter as tk
from tkinter import messagebox
from ui.utils import center_window
from models.redemption import Redemption


def show_category_screen(root, client, category):
    screen = tk.Toplevel(root)
    screen.title("Επιλογή Ανταμοιβής")
    screen.geometry("600x500")
    center_window(screen)
    screen.config(bg="#22A298")

    top_frame = tk.Frame(screen, bg="#166A64")
    top_frame.pack(fill=tk.X, pady=5)

    tk.Label(top_frame, text=f"Κατηγορία: {category}", font=("Arial", 14, "bold"),
             bg="#166A64", fg="white").pack(side=tk.LEFT, padx=10)

    tk.Label(screen, text="Επέλεξε Ανταμοιβή", font=("Arial", 14, "bold"),
             bg="#22A298", fg="black").pack(pady=20)

    valid_options = [
        "Εισιτήριο Γενικής Εισόδου",
        "VIP Πρόσκληση",
        "Κουπόνι Φαγητού & Ποτού",
        "Ειδικό Αναμνηστικό Δώρο",
        "Αναβάθμιση Εισιτηρίου",
        "Συμμετοχή σε Κλήρωση Δώρων"
    ]

    expired_options = {
        "VIP Πρόσκληση",
        "Ειδικό Αναμνηστικό Δώρο"
    }

    def redeem(option):
        result = client.make_selection(category, option)

        if result["status"] == "expired":
            messagebox.showinfo("Μη διαθέσιμη επιλογή", result["message"])
            return

        if client.points_system.deduct_points(50):
            redemption_id = len(client.redemptions) + 1
            redemption = Redemption(redemption_id, category, option)
            redemption.redeem_points()
            client.redemptions.append(redemption)
            messagebox.showinfo("Επιτυχία", "Η εξαργύρωση ολοκληρώθηκε.")
            screen.destroy()
        else:
            messagebox.showerror("Αποτυχία", "Δεν υπάρχουν αρκετοί πόντοι.")

    for option in valid_options:
        tk.Button(screen, text=option, font=("Arial", 12, "bold"),
                  bg="black", fg="#DDB0B0", width=30,
                  state=tk.NORMAL,
                  command=lambda opt=option: redeem(opt)).pack(pady=5)

    screen.mainloop()
