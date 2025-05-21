import tkinter as tk
from tkinter import messagebox
from ui.categories_screen import show_categories_screen
from ui.utils import center_window


def show_points_screen(root, controller):
    # Υπολογισμός πόντων
    controller.client.points_system.calculate_points()
    points = controller.client.points_system.show_points()

    if controller.client.points_system.check_balance():
        # Επαρκείς πόντοι => συνέχισε στη λίστα κατηγοριών
        show_categories_screen(root, controller)
    else:
        # Μη επαρκείς πόντοι => δείξε error
        messagebox.showerror("Μη επαρκείς πόντοι", "Δεν έχετε αρκετούς πόντους για εξαργύρωση.")
