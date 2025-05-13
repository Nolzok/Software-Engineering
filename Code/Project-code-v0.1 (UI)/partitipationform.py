import tkinter as tk

def create_gradient(canvas, width, height, color1, color2):
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    for i in range(height):
        r = r1 + (r2 - r1) * i // height
        g = g1 + (g2 - g1) * i // height
        b = b1 + (b2 - b1) * i // height
        hex_color = f'#{r//256:02x}{g//256:02x}{b//256:02x}'
        canvas.create_line(0, i, width, i, fill=hex_color)

class UIapp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Unignite")
        self.root.geometry("1200x800")

        self.canvas = tk.Canvas(self.root, width=1200, height=800)
        self.canvas.pack(fill="both", expand=True)
        create_gradient(self.canvas, 1200, 800, "#22A298", "#FFC0CB")

        self.show_event_screen()

    def clear_frame(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

    def show_event_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.canvas, bg="#FFC0CB")
        frame.place(relx=0.5, rely=0.2, anchor="center")
        tk.Label(frame, text="Εκδήλωση: Καλοκαιρινή Εκδήλωση",
                 font=("Helvetica", 20, "bold italic"), bg="#FFC0CB", fg="#333").pack(pady=10)

        tk.Button(frame, text="Δήλωση Ενδιαφέροντος", font=("Helvetica", 16, "bold"),
                  command=self.show_seat_screen, bg="#ff99cc", fg="white", bd=0,
                  relief="flat", padx=10, pady=5).pack(pady=10)

    def show_seat_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.canvas, bg="#FFC0CB")
        frame.place(relx=0.5, rely=0.3, anchor="center")

        tk.Label(frame, text="Θέσεις διαθέσιμες: 3", font=("Helvetica", 16),
                 bg="#FFC0CB", fg="#333").pack(pady=10)
        tk.Button(frame, text="Κράτηση Θέσης", font=("Helvetica", 14, "bold"),
                  command=self.show_form_screen, bg="#ff6688", fg="white", bd=0,
                  relief="flat", padx=10, pady=5).pack(pady=10)

    def show_form_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.canvas, bg="#FFFFFF", bd=2, relief="ridge")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=600)

        self.fields = {}
        for label in ["Ονοματεπώνυμο", "Ηλικία", "Τηλέφωνο", "Email"]:
            self.add_entry(frame, label)

        for label in ["Ενδιαφέροντα/Προτιμήσεις", "Διατροφικές προτιμήσεις/αλλεργίες", "Ειδικές ανάγκες ή αιτήματα"]:
            self.add_text(frame, label)


        tk.Button(frame, text="Submit", font=("Helvetica", 14, "bold"), bg="#66ccff", fg="white",
                  bd=0, relief="flat", padx=10, pady=5).pack(pady=10)

    def add_entry(self, parent, label):
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.pack(fill="x", pady=5, padx=20)
        tk.Label(frame, text=label, bg="#FFFFFF", font=("Helvetica", 12)).pack(anchor="w")
        entry = tk.Entry(frame, bg="#f0f0f0", relief="flat", font=("Helvetica", 12))
        entry.pack(fill="x")

    def add_text(self, parent, label):
        frame = tk.Frame(parent, bg="#FFFFFF")
        frame.pack(fill="x", pady=5, padx=20)
        tk.Label(frame, text=label, bg="#FFFFFF", font=("Helvetica", 12)).pack(anchor="w")
        text = tk.Text(frame, height=3, bg="#f0f0f0", relief="flat", font=("Helvetica", 12))
        text.pack(fill="x")

if __name__ == "__main__":
    UIapp().root.mainloop()
