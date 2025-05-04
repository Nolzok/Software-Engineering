import tkinter as tk
from tkinter import ttk

user_points = 120
extra_points = 30
max_points = 200


root = tk.Tk()
root.title("Σύστημα Επιβράβευσης")
root.geometry("600x500")
root.config(bg="#22A298")


style = ttk.Style()
style.theme_use("default")
style.configure("pink.Horizontal.TProgressbar", troughcolor="#FFFFFF", background="#DDB0B0", thickness=20)


top_frame = tk.Frame(root, bg="#166A64")
top_frame.pack(fill=tk.X, pady=5)

tk.Button(top_frame, text="Εξαργύρωση", font=("Arial", 10, "bold"),
          bg="black", fg="#DDB0B0").pack(side=tk.RIGHT, padx=10)

# Τίτλος
title_frame = tk.Frame(root, bg="black", padx=20, pady=10)
title_frame.pack(pady=10, anchor="center")

title_label = tk.Label(title_frame, text="Οι Πόντοι μου", font=("Arial", 15, "bold"),
                       bg="black", fg="#DDB0B0")
title_label.pack()

# Πόντοι
points_frame = tk.Frame(root, bg="#22A298")
points_frame.pack(pady=10, padx=30, anchor="w")

# Συνολικοί Πόντοι
tk.Label(points_frame, text="Συνολικοί Πόντοι", font=("Arial", 14),
         bg="#22A298", fg="black").grid(row=0, column=0, sticky="w", pady=2)
ttk.Progressbar(points_frame, length=250, mode='determinate',
                maximum=max_points, value=user_points,
                style="pink.Horizontal.TProgressbar").grid(row=1, column=0, sticky="w")
tk.Label(points_frame, text=f"{user_points}/{max_points}", font=("Arial", 12),
         bg="#22A298", fg="black").grid(row=1, column=1, padx=10)

# Extra Πόντοι
tk.Label(points_frame, text="Extra Πόντοι", font=("Arial", 14),
         bg="#22A298", fg="black").grid(row=2, column=0, sticky="w", pady=(15, 2))
ttk.Progressbar(points_frame, length=250, mode='determinate',
                maximum=max_points, value=extra_points,
                style="pink.Horizontal.TProgressbar").grid(row=3, column=0, sticky="w")
tk.Label(points_frame, text=f"{extra_points}/{max_points}", font=("Arial", 12),
         bg="#22A298", fg="black").grid(row=3, column=1, padx=10)

# Κατηγορίες
categories_frame = tk.Frame(root, bg="#22A298")
categories_frame.pack(pady=10, padx=30, anchor="w")

category_title = tk.Label(categories_frame, text="Κατηγορίες Εξαργύρωσης", font=("Arial", 14, "bold"),
                          bg="#22A298", fg="black")
category_title.pack(anchor="w", pady=10)

categories_listbox = tk.Listbox(categories_frame, font=("Arial", 12), height=6,
                                bg="#DDB0B0", fg="black", selectbackground="white", width=30)
categories_listbox.pack()

for category in ["Αθλητικά", "Τεχνολογία", "Περιβάλλον", "Πολιτισμός"]:
    categories_listbox.insert(tk.END, category)

root.mainloop()
