import tkinter as tk

# Παράθυρο φόρμας δημιουργίας event
form = tk.Tk()
form.title("Δημιουργία Event")
form.geometry("600x720")
form.configure(bg="#22A298")

# Τίτλος φόρμας
title = tk.Label(form, text="Δημιουργία νέου event", font=("Arial", 16, "bold"), bg="#22A298", fg="black")
title.pack(pady=20)

# Λίστα πεδίων
labels = [
    "Όνομα", "Τοποθεσία", "Ημερομηνία & Ώρα", "Κατηγορία", "Διάρκεια", "Περιγραφή",
    "Τιμή", "Μέγιστος αριθμός συμμετεχόντων"
]

entries = {}

# Φόρμα πεδίων
for label_text in labels:
    label = tk.Label(form, text=label_text, bg="#22A298", fg="black", anchor="w", font=("Arial", 9, "bold"))
    label.pack(fill="x", padx=40, pady=(10, 0))

    if label_text == "Περιγραφή":
        entry = tk.Text(form, bg="#DDB0B0", fg="black", relief="flat", font=("Arial", 15), height=4)
        entry.pack(fill="x", padx=40)
    else:
        entry = tk.Entry(form, bg="#DDB0B0", fg="black", relief="flat", font=("Arial", 15))
        entry.pack(fill="x", padx=40)

    entries[label_text] = entry

# Κουμπί δημιουργίας
submit_button = tk.Button(
    form, text="Δημιουργία Event",
    bg="#166A64", fg="white",
    font=("Arial", 15, "bold")
)
submit_button.pack(pady=30)

form.mainloop()
