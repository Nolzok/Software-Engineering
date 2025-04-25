import tkinter as tk

# αρχικο παραθυρο
root = tk.Tk()
root.title("Οθόνη με Events διοργανωτή")
root.geometry("600x450")
root.config(bg="#22A298")  

# πλαίσιο (για κουμπί)
top_frame = tk.Frame(root, bg="#166A64")  
top_frame.pack(fill=tk.X, pady=5)

# κουμπι για δημιουργια new event πάνω δεξιά
tk.Button(top_frame, text="Νέο Event", font=("Arial", 10, "bold"), bg="black", fg="#DDB0B0").pack(side=tk.RIGHT, padx=10)

# "Τα events μου" σε μαύρο πλαίσιο
title_frame = tk.Frame(root, bg="black", padx=20, pady=10)
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="Τα events μου", font=("Arial", 15, "bold"), bg="black", fg="#DDB0B0")
title_label.pack()

# λίστα με events 
event_listbox = tk.Listbox(root, font=("Arial", 16), height=20, selectbackground="white", activestyle="none", bg="#DDB0B0", fg="black")
event_listbox.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

#  events για το UI
dummy_events = [
    "1. Φεστιβάλ Τεχνολογίας",
    "2. Ημέρα Περιβάλλοντος",
    "3. Startup Meetup",
    "4. Βραδιά Κινηματογράφου",
    "5. Σεμινάριο Photoshop",
    "6. Γιορτή Βιβλίου",
    "7. Περίπατος Υγείας",
    "8. Coding Bootcamp"
]

for event in dummy_events:
    event_listbox.insert(tk.END, event)

root.mainloop()
