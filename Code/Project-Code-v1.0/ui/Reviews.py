from telnetlib import DO
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  
from database.database import connect_to_mysql, Database
from ui.utils import center_window
from ui.lostItems import LostItemsApp
from ui.profile_screen import ProfileScreen
from ui.home_screen_points import run_home_screen
import os

def selectReviews():
    conn, cursor = connect_to_mysql()
    cursor.execute("SELECT username, user_id FROM users WHERE user_id = 1")
    username, uid = cursor.fetchone()
    cursor.close(); conn.close()
    
    root = tk.Tk()
    root.title("Home Page")
    root.geometry("700x600")
    
    style = ttk.Style(root)
    style.theme_use("default")
    style.configure("pink.Horizontal.TProgressbar",
                    troughcolor="#FFFFFF",
                    background="#DDB0B0",
                    thickness=20)
    
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
    def do_nothing(): pass
    def open_profile():
        profile_window = tk.Toplevel(root)
        db = Database()
        ProfileScreen(profile_window, db)
    
    for text, cmd in [
        ("Σύστημα Επιβράβευσης", run_home_screen),
        ("Προφίλ", open_profile),
        ("Κριτικές-Αξιολογήσεις", do_nothing),
        ("Δωρεές", selectReviews),
        ("Πρόσκληση Φίλων", do_nothing),
        ("Χαμένα Αντικείμενα", app.create_main_screen),
        ("Ειδοποιήσεις", do_nothing),
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
    
    def clear_content():
        for w in content.winfo_children():
            w.destroy()
    
    def choose_category():
        clear_content()
        tk.Label(content,
                 text="Επιλέξτε Κατηγορία:",
                 font=("Times", 20, "bold"),
                 bg="#22A298").pack(pady=10)
        
        conn, cursor = connect_to_mysql()
        cursor.execute("SELECT DISTINCT Category FROM post")
        categories = [row[0] for row in cursor.fetchall()]
        cursor.close(); conn.close()
        
        combo = ttk.Combobox(content, values=categories, state="readonly", font=("Arial", 14))
        combo.pack(pady=5)
        tk.Button(content,
                  text="Επόμενο",
                  font=("Times", 12),
                  bg="#DDB0B0",
                  command=lambda: choose_subcategory(combo.get())
                 ).pack(pady=10)
    
    def choose_subcategory(category):
        clear_content()
        tk.Label(content,
                 text=f"Κατηγορία: {category}",
                 font=("Times", 18, "bold"),
                 bg="#22A298").pack(pady=(10,5))
        tk.Label(content,
                 text="Επιλέξτε Υποκατηγορία:",
                 font=("Times", 16),
                 bg="#22A298").pack(pady=5)
        
        conn, cursor = connect_to_mysql()
        cursor.execute("SELECT DISTINCT Sub_Category FROM post WHERE Category = %s", (category,))
        subs = [row[0] for row in cursor.fetchall()]
        cursor.close(); conn.close()
        
        combo = ttk.Combobox(content, values=subs, state="readonly", font=("Arial", 14))
        combo.pack(pady=5)
        tk.Button(content,
                  text="Προβολή Ανακοινώσεων",
                  font=("Times", 12),
                  bg="#DDB0B0",
                  command=lambda: show_posts(category, combo.get())
                 ).pack(pady=10)
    
    def show_posts(category, sub_category):
        clear_content()
        conn, cursor = connect_to_mysql()
        cursor.execute("""
            SELECT id, title, description, requiredPoints, Category, Sub_Category
            FROM post
            WHERE Category = %s AND Sub_Category = %s
        """, (category, sub_category))
        posts = cursor.fetchall()
        cursor.close(); conn.close()
        
        if not posts:
            tk.Label(content,
                     text="No posts available.",
                     font=("Arial", 14),
                     bg="#22A298",
                     fg="black").pack(pady=20)
            return
        
        for post_id, title, description, points, cat, sub in posts:
            post_frame = tk.LabelFrame(
                content,
                text="",
                font=("Arial", 14, "bold"),
                bg="#22A298",
                fg="black",
                padx=10,
                pady=5,
                borderwidth=2
            )
            post_frame.pack(fill="x", padx=20, pady=10)
            
            lbl = tk.Label(post_frame,
                           text=title,
                           font=("Arial", 14, "bold"),
                           bg="#22A298",
                           fg="black",
                           cursor="hand2")
            lbl.pack(anchor="w")
            lbl.bind("<Button-1>", lambda e, pid=post_id: viewDetails(pid, uid, content))
            
            tk.Label(post_frame,
                     text=description,
                     font=("Arial", 12),
                     bg="#22A298",
                     fg="black",
                     wraplength=800,
                     justify="left"
            ).pack(anchor="w", pady=(0, 5))
            
            info = f"Required Points: {points} | Category: {cat}/{sub}"
            tk.Label(post_frame,
                     text=info,
                     font=("Arial", 11, "italic"),
                     bg="#22A298",
                     fg="#555555"
            ).pack(anchor="e")
    
    choose_category()
    root.mainloop()








     
def viewDetails(post_id, uid, content):
    for widget in content.winfo_children():
        widget.destroy()
    
     
        conn, cursor = connect_to_mysql()
        cursor.execute("SELECT * FROM post WHERE id = %s", (post_id,))
        post = cursor.fetchone()
    
     
        cursor.execute("SELECT totalpoints FROM pointsystem WHERE clientID = 1")
        total_points = cursor.fetchone()[0]
        cursor.execute("SELECT username FROM users WHERE user_id = 1")
        username = cursor.fetchone()[0]
        cursor.close()
        conn.close()

     
        details_frame = tk.Frame(content, bg="#22A298")
        details_frame.pack(fill="both", expand=True, padx=20, pady=20)

     
        back_button = tk.Button(details_frame, text="Back", 
                          command=lambda: [details_frame.destroy(), selectReviews()],
                          bg="#DDB0B0", fg="black")
        back_button.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

             
        tk.Label(details_frame, text=post[1], font=("Arial", 16, "bold"), 
               bg="#22A298", fg="black").grid(row=1, column=0, columnspan=2, sticky="w")
    
         
        forms_container = tk.Frame(details_frame, bg="#22A298")
        forms_container.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=20)

         
         
        left_form = tk.LabelFrame(forms_container, text="Points Transfer",
                                font=("Arial", 12, "bold"),
                                bg="#22A298", fg="black")
        left_form.grid(row=0, column=0, padx=10, sticky="nsew")
    

         
        tk.Label(left_form, text=f"Available Points: {total_points}", 
               font=("Arial", 10), bg="#22A298").grid(row=0, column=0, columnspan=2, pady=5)

         
        tk.Label(left_form, text="Points to Transfer:", 
               font=("Arial", 10), bg="#22A298").grid(row=1, column=0, pady=5)
        points_entry = tk.Entry(left_form, width=15)
        points_entry.grid(row=1, column=1, pady=5)

         
        tk.Button(left_form, text="Submit Points",
                 command=lambda: submit_points(
                      points_entry,
                       post_required_points=post[3],
                       client_id=uid,
                       post_id=post_id
                   ),
                bg="#DDB0B0", fg="black").grid(row=2, column=0, columnspan=2, pady=10)

         
        left_form.columnconfigure(1, weight=1)
        


        right_form = tk.LabelFrame(forms_container, text="User Details",
                                 font=("Arial", 12, "bold"),
                                 bg="#22A298", fg="black")
        right_form.grid(row=0, column=1, padx=10, sticky="nsew")

         
        tk.Label(right_form, text="Username:", 
               font=("Arial", 10), bg="#22A298").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        username_entry = tk.Entry(right_form, width=20)
        username_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

         
        tk.Label(right_form, text="16-Digit Code:", 
               font=("Arial", 10), bg="#22A298").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        code16_entry = tk.Entry(right_form, validate="key")
        code16_entry['validatecommand'] = (code16_entry.register(lambda P: P.isdigit() and len(P) <= 16), '%P')
        code16_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    
      
        tk.Label(right_form, text="3-Digit Code:", 
               font=("Arial", 10), bg="#22A298").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        code3_entry = tk.Entry(right_form, validate="key")
        code3_entry['validatecommand'] = (code3_entry.register(lambda P: P.isdigit() and len(P) <= 3), '%P')
        code3_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

         
        tk.Label(right_form, text="Amount:", 
               font=("Arial", 10), bg="#22A298").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        amount_entry = tk.Entry(right_form, validate="key")
        amount_entry['validatecommand'] = (amount_entry.register(lambda P: P.isdigit()), '%P')
        amount_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

         
        tk.Button(right_form, text="Submit Details",
           command=lambda: submit_user_details(
               username_entry,
               code16_entry,
               code3_entry,
               amount_entry,
               client_id=uid,
               post_id=post_id
           ),
                bg="#DDB0B0", fg="black").grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

         
        right_form.columnconfigure(1, weight=1)
        details_frame.columnconfigure(0, weight=1)
        forms_container.columnconfigure(0, weight=1)
        forms_container.columnconfigure(1, weight=1)


def submit_points(points_entry, post_required_points, client_id, post_id):
    try:
        print("submit_points klithike:", client_id, post_id)
        points = int(points_entry.get())
        if points <= 0:
            raise ValueError("Please enter a positive number")

        conn, cursor = connect_to_mysql()
        cursor.execute(
            "SELECT totalpoints FROM pointsystem WHERE clientID = %s",
            (client_id,)
        )
        available_points = cursor.fetchone()[0]
        if available_points < points:
            raise ValueError("Insufficient points balance")

        cursor.execute(
            "UPDATE pointsystem SET totalpoints = totalpoints - %s WHERE clientID = %s",
            (points, client_id)
        )

        print(f"(PointExchange): client={client_id}, post={post_id}, pts={points}")
        cursor.execute("""
            INSERT INTO donation
                (client_id, post_id, date, methodUsed, pointsUsed)
            VALUES (%s, %s, CURDATE(), 'PointExchange', %s)
        """, (client_id, post_id, points))

        conn.commit()
        print("test passed")

        messagebox.showinfo("Success", f"{points} points submitted successfully!")
        selectReviews()

    except Exception as e:
        import traceback; traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def submit_user_details(username_entry, code16_entry, code3_entry, amount_entry, client_id, post_id):
    try:
        conn, cursor = connect_to_mysql()
        
         
        entered_username = username_entry.get().strip()
        
         
        cursor.execute("SELECT username FROM users WHERE user_id = %s", (client_id,))
        result = cursor.fetchone()
        
        if not result:
            messagebox.showerror("Error", "User not found")
            return
            
        actual_username = result[0]
        
         
        if entered_username.lower() != actual_username.lower():
            messagebox.showerror("Error", "Incorrect username")
            return

         
        code16 = code16_entry.get()
        if len(code16) != 16 or not code16.isdigit():
            messagebox.showerror("Error", "Invalid 16-digit code")
            return
            
        code3 = code3_entry.get()
        if len(code3) != 3 or not code3.isdigit():
            messagebox.showerror("Error", "Invalid 3-digit code")
            return
            
        amount = amount_entry.get()
        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Error", "Invalid amount")
            return

         
        messagebox.showinfo("Success", "Details submitted successfully!")
         
        
        cursor.execute("""
            INSERT INTO donation
                 (client_id, post_id, date, methodUsed, pointsUsed)
            VALUES (%s, %s, CURDATE(), 'CardInfo', %s)
        """, (client_id, post_id, amount))
        conn.commit()


    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

