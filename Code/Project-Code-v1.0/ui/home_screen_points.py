import tkinter as tk
from tkinter import ttk
from controllers.reward_controller import RewardController
from ui.utils import center_window
from PIL import Image, ImageTk  
import os



def run_home_screen():
    controller = RewardController()
    controller.client.points_system.total_points = 120
    controller.client.points_system.extra_points = 30

    root = tk.Tk()
    root.title("Σύστημα Επιβράβευσης")
    root.geometry("600x500")
    center_window(root)
    root.config(bg="#22A298")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("pink.Horizontal.TProgressbar", troughcolor="#FFFFFF", background="#DDB0B0", thickness=20)

    top_frame = tk.Frame(root, bg="#166A64")
    top_frame.pack(fill=tk.X, pady=5)

    def on_redemption_click():
        controller.handle_redemption_click(root)

    tk.Button(top_frame, text="Εξαργύρωση", font=("Arial", 10, "bold"),
              bg="black", fg="#DDB0B0", command=on_redemption_click).pack(side=tk.RIGHT, padx=10)

    # Πόντοι
    points_frame = tk.Frame(root, bg="#22A298")
    points_frame.pack(pady=10, padx=30, anchor="w")

    tk.Label(points_frame, text="Συνολικοί Πόντοι", font=("Arial", 14),
             bg="#22A298", fg="black").grid(row=0, column=0, sticky="w", pady=2)
    ttk.Progressbar(points_frame, length=250, mode='determinate',
                    maximum=200, value=controller.client.points_system.total_points,
                    style="pink.Horizontal.TProgressbar").grid(row=1, column=0, sticky="w")
    tk.Label(points_frame, text=f"{controller.client.points_system.total_points}/200", font=("Arial", 12),
             bg="#22A298", fg="black").grid(row=1, column=1, padx=10)

    tk.Label(points_frame, text="Extra Πόντοι", font=("Arial", 14),
             bg="#22A298", fg="black").grid(row=2, column=0, sticky="w", pady=(15, 2))
    ttk.Progressbar(points_frame, length=250, mode='determinate',
                    maximum=200, value=controller.client.points_system.extra_points,
                    style="pink.Horizontal.TProgressbar").grid(row=3, column=0, sticky="w")
    tk.Label(points_frame, text=f"{controller.client.points_system.extra_points}/200", font=("Arial", 12),
             bg="#22A298", fg="black").grid(row=3, column=1, padx=10)

    bottom_frame = tk.Frame(root, bg="#22A298")
    bottom_frame.pack(pady=20)

    current_dir = os.path.dirname(os.path.abspath(__file__))  # directory του home_screen.py
    assets_dir = os.path.abspath(os.path.join(current_dir, '..', 'assets'))
    img_path = os.path.join(assets_dir, "reward1.jpg")

    tk.Label(bottom_frame, text="Κερδίστε πόντους και εξαργυρώστε για μοναδικά δώρα!",
             font=("Arial", 12, "italic"), bg="#22A298", fg="black").pack(pady=10)

    try:
        pil_img = Image.open(img_path)
        max_width, max_height = 350, 250
        pil_img = pil_img.resize((max_width, max_height), Image.LANCZOS)


        reward_img = ImageTk.PhotoImage(pil_img)
        img_label = tk.Label(bottom_frame, image=reward_img, bg="#22A298")
        img_label.image = reward_img 
        img_label.pack()
    except Exception as e:
        print("Η εικόνα δεν φορτώθηκε:", e)

    

    root.mainloop()
