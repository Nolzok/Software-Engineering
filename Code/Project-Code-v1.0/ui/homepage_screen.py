import tkinter as tk
from ui.profile_screen import ProfileScreen   

class HomepageScreen:
    def __init__(self, root, database):
        self.root = root       
        self.db = database     
        self.build_homepage()  

    def build_homepage(self):
        self.root.title("Homepage")              
        self.root.geometry("600x400")            

        
         
        tk.Button(
            self.root,
            text="👤",    
            command=self.open_profile_screen,   
            bg="#22A298", fg="white", font=("Arial", 14)
        ).pack()

    def open_profile_screen(self):
         
        for widget in self.root.winfo_children():
            widget.destroy()
         
        ProfileScreen(self.root, self.db)
