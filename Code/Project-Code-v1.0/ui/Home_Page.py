 
import tkinter as tk
from tkinter import ttk
 
from ui.utils import center_window
from PIL import Image, ImageTk  
from database.database import connect_to_mysql
from database.database import Database
from ui.home_screen_points import run_home_screen
from ui.Reviews import selectReviews
from ui.lostItems import LostItemsApp
from ui.profile_screen import ProfileScreen
from ui.search import make_event_search_bar, EventApp
from ui.Donations import show_reviews_screen
from ui.Friends import FriendsSystem, FriendsPage, NotificationSystem, NotificationsPage
from database.db_config import DB_CONFIG
import os



def run_home_page_screen():
    
    conn, cursor = connect_to_mysql()
     
    cursor.execute("SELECT username, user_id FROM users WHERE user_id = 1")
    result = cursor.fetchone()
    username, uid = result
    cursor.close()
    conn.close()


    root=tk.Tk()  
    root.title("Home Page")
    root.geometry("700x600")  
     
    style = ttk.Style(root)
    style.theme_use("default")
    style.configure("pink.Horizontal.TProgressbar",
                    troughcolor="#FFFFFF",
                    background="#DDB0B0",
                    thickness=20)


    content = tk.Frame(root, bg="white")
    content.grid(row=1, column=1, sticky="nsew", padx=(5,10), pady=10)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)  

     
    header = tk.Frame(root, bg="#166A64", height=60)
    header.grid(row=0, column=0, columnspan=2, sticky="nsew")
    header.grid_propagate(False)
    tk.Label(header,
             text=f'Welcome {username} (ID:{uid}) to Unignite!',
             font=("Comic Sans MS", 20),
             bg="#166A64",
             fg="white").pack(side="left", padx=20)

     
    sidebar = tk.Frame(root, bg="#133F3F", width=300)
    sidebar.grid(row=1, column=0, sticky="nsew", padx=(10,5), pady=10)
    sidebar.grid_propagate(False)
    tk.Label(sidebar,
             text="Menu",
             font=("Arial", 16, "bold"),
             bg="#133F3F",
             fg="white").pack(pady=(10,20))
    
    
    app = LostItemsApp(root)
    
    def clear_content():
        for w in content.winfo_children():
            w.destroy()

    def open_friends():
        clear_content()
        fs = FriendsSystem(DB_CONFIG)
        friends_page = FriendsPage(content, fs, uid)
        friends_page.pack(fill=tk.BOTH, expand=True)

    def open_notifications():
        clear_content()
        fs = FriendsSystem(DB_CONFIG)
        ns = NotificationSystem(fs.cursor)
        notif_page = NotificationsPage(content, ns, uid)
        notif_page.show()
        notif_page.pack(fill=tk.BOTH, expand=True)

    def do_nothing():
        pass
    
    def open_profile():
         
        profile_window = tk.Toplevel(root)
        db = Database()
        ProfileScreen(profile_window, db)
        
    for text,cmd in [
        ("Σύστημα Επιβράβευσης",run_home_screen),  
        ("Προφίλ",open_profile),
        ("Κριτικές-Αξιολογήσεις",lambda: show_reviews_screen(root)),
        ("Δωρεές",selectReviews),
        ("Πρόσκληση Φίλων",open_friends),
        ("Χαμένα Αντικείμενα",app.create_main_screen),
        ("Ειδοποιήσεις",open_notifications)
    ]:
    
        tk.Button(sidebar,
                  text=text,
                  font=("Times", 14),
                  bg="#DDB0B0",
                  fg="black",
                  width=20,
                  command=cmd).pack(pady=5)  

     
    content = tk.Frame(root, bg="#22A298")
    content.grid(row=1, column=1, sticky="nsew", padx=(5,10), pady=10)

    intro = "Καλώς ήρθατε! Αναζητήστε εκδηλώσεις εδώ:"
    tk.Label(content,
             text=intro,
             font=("Times", 16),
             bg="#22A298",
             fg="black",
             justify="left") \
      .pack(anchor="nw", padx=20, pady=20)

    def launch_search(keyword):
        win = tk.Toplevel(root)
        app = EventApp(win)
        app.search_var.set(keyword)
        app.search_keywords()

    def launch_filter():
        win = tk.Toplevel(root)
        app = EventApp(win)
        app.show_filters()

    make_event_search_bar(
        parent=content,
        search_callback=launch_search,
        filter_callback=launch_filter)



     
     

    root.mainloop()
