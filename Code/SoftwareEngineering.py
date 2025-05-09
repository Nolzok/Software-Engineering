import tkinter as tk

# Αρχικό παράθυρο
root = tk.Tk()
root.title("Donation Screen")
root.geometry("600x450")
root.config(bg="#22A298")  

# Πλαίσιο (για κουμπί)
top_frame = tk.Frame(root, bg="#166A64")  
top_frame.pack(fill=tk.X, pady=5)

# Κουμπί για δημιουργία new event πάνω δεξιά
#tk.Button(top_frame, text="Tree Planting", font=("Arial", 10, "bold"), 
#        bg="black", fg="#DDB0B0").pack(side=tk.RIGHT, padx=10)

# "Τα events μου" σε μαύρο πλαίσιο
title_frame = tk.Frame(root, bg="black", padx=20, pady=10)
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="Event Categories", 
                      font=("Arial", 15, "bold"), bg="black", fg="#DDB0B0")
title_label.pack()

# Create a container for buttons with scrollbar
container = tk.Frame(root, bg="#22A298")
container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

# Create canvas and scrollbar
canvas = tk.Canvas(container, bg="#DDB0B0")
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#DDB0B0")

# Configure scrolling
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Δημιουργία κουμπιών
"""
dummy_events = [
    "1. Tree Planting",
    "2. Animal Shelters",
    "3. Supplies for Homeless People",
    "4. Beach Cleaning Equipment"
]
    """
    
dummy_events = [
    "1. Animal Category",
    "2. Children in Need",
    "3. Refugees in Need",
    "4. Environmental Protection"
]

for idx, event in enumerate(dummy_events):
    row = idx // 2
    col = idx % 2
    btn = tk.Button(
        scrollable_frame,
        text=event,
        font=("Arial", 12),
        bg="#DDB0B0",
        fg="#22A298",
        anchor="w",
        padx=10,
        pady=5,
        width=25  # Fixed width for consistent appearance
    )
    btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

root.mainloop()