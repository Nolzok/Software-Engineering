from telnetlib import DO
import tkinter as tk
from tkinter import ttk
from controllers.reward_controller import RewardController
from ui.utils import center_window
from PIL import Image, ImageTk  
from database.database import connect_to_mysql
from ui.home_screen_points import run_home_screen
import os



def run_home_page_screen():
    
    conn, cursor = connect_to_mysql()
     
    cursor.execute("SELECT username, user_id FROM users WHERE user_id = 1")
    result = cursor.fetchone()
    username, uid = result
    cursor.close()
    conn.close()


    controller = RewardController()
    controller.client.points_system.total_points = 120
    controller.client.points_system.extra_points = 30
    root=tk.Tk() #ftiaxnoume to arxiko window
    root.title("Home Page")
    root.geometry("1600x1000") #orizoume to size tou arxikou window
    #center_window(root)
    style = ttk.Style(root)
    style.theme_use("default")
    style.configure("pink.Horizontal.TProgressbar",
                    troughcolor="#FFFFFF",
                    background="#DDB0B0",
                    thickness=20)

    # ——— Grid config ———
    root.grid_rowconfigure(1, weight=1)       # make row 1 grow
    root.grid_columnconfigure(1, weight=1)    # make column 1 grow

    # ——— Header ———
    header = tk.Frame(root, bg="#166A64", height=60)
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")
    header.grid_propagate(False)
    tk.Label(header,
             text=f'Welcome {username} (ID:{uid}) to Unignite!',
             font=("Comic Sans MS", 20),
             bg="#166A64",
             fg="white").pack(side="left", padx=20)

    #tk.Button(header,
    #          text="Εξαργύρωση",
    #          font=("Arial", 10, "bold"),
    #          bg="black",
    #          fg="#DDB0B0",
    #          command=run_home_screen).pack(side="right", padx=20)

    # ——— Sidebar navigation ———
    sidebar = tk.Frame(root, bg="#133F3F", width=300)
    sidebar.grid(row=1, column=0, sticky="nsew", padx=(10,5), pady=10)
    sidebar.grid_propagate(False)
    tk.Label(sidebar,
             text="Menu",
             font=("Arial", 16, "bold"),
             bg="#133F3F",
             fg="white").pack(pady=(10,20))
    # example buttons
    #for text, cmd in [ #command = cmd pou simainei oti command=do_something()
    #("Basic Statistics", do_first_question),
    #    ("Months + Seasons", do_second_question),
    #    ("Rooms", do_third_question),
    #    ("Family", do_fourth_question),
    #    ("Tendencies", do_fifth_question),
    #    ("Frequency", do_sixth_question),
    #]:m
    def do_nothing():
        pass
    for text,cmd in [
        ("Σύστημα Επιβράβευσης",run_home_screen), #Συστημα Επιβράβευσης #Προφίλ #Κριτικές-Αξιολογήσεις #Δωρεές #Πρόσκληση Φίλων #Χαμένα Αντικείμενα #Ειδοποιήσεις
        ("Προφίλ",do_nothing),
        ("Κριτικές-Αξιολογήσεις",do_nothing),
        ("Δωρεές",do_nothing),
        ("Πρόσκληση Φίλων",do_nothing),
        ("Χαμένα Αντικείμενα",do_nothing),
        ("Ειδοποιήσεις",do_nothing)
    ]:
    
        tk.Button(sidebar,
                  text=text,
                  font=("Times", 14),
                  bg="#DDB0B0",
                  fg="black",
                  width=20,
                  command=cmd).pack(pady=5) #otan to allaxo tha prepei na leei command = cmd

    # ——— Main content area ———
    content = tk.Frame(root, bg="#22A298")
    content.grid(row=1, column=1, sticky="nsew", padx=(5,10), pady=10)

    intro = (
        "ΕΔΏ ΘΑ ΜΠΕΙ Η ΜΠΆΡΑ ΑΝΑΖΉΤΗΣΗΣ."
    )
    tk.Label(content,
             text=intro,
             font=("Times", 16),
             bg="#22A298",
             fg="black",
             justify="left").pack(anchor="nw", padx=20, pady=20)

    # — example progress bars —
    pts = controller.client.points_system
    for label_text, value in [
        ("Total Points", pts.total_points),
        ("Extra Points", pts.extra_points)
    ]:
        frame = tk.Frame(content, bg="#22A298")
        frame.pack(fill="x", padx=20, pady=(10,5))
        tk.Label(frame,
                 text=label_text,
                 font=("Arial", 14),
                 bg="#22A298",
                 fg="black").pack(anchor="w")
        bar = ttk.Progressbar(frame,
                              length=300,
                              mode='determinate',
                              maximum=200,
                              value=value,
                              style="pink.Horizontal.TProgressbar")
        bar.pack(side="left", pady=5)
        tk.Label(frame,
                 text=f"{value}/200",
                 font=("Arial", 12),
                 bg="#22A298",
                 fg="black").pack(side="left", padx=10)

    # ——— Footer or image ———
    # (You can add your PIL image here, same as before)

    root.mainloop()
