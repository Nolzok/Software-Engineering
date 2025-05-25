from telnetlib import DO
import tkinter as tk
from tkinter import ttk
from database.database import connect_to_mysql
import os

def show_reviews_screen(parent=None):
     
    conn, cursor = connect_to_mysql()
    cursor.execute("SELECT username, user_id FROM users WHERE user_id = 1")
    result = cursor.fetchone()
    username, uid = result
    cursor.close()
    conn.close()

     
    if parent:
        window = tk.Toplevel(parent)
    else:
        window = tk.Tk()
    window.title("Κριτικές και Αξιολογήσεις")
    window.geometry("900x600")

     
    main_frame = tk.Frame(window, bg="#22A298")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    def show_previous_reviews():
         
        for widget in main_frame.winfo_children():
            widget.destroy()

         
        tk.Label(main_frame,
                text="Οι Κριτικές σας",
                font=("Times", 20, "bold"),
                bg="#22A298").pack(pady=10)

         
        conn, cursor = connect_to_mysql()
        cursor.execute("""
            SELECT r.content, e.name 
            FROM review r
            JOIN events e ON r.event_id = e.eventID
            WHERE r.client_id=%s
        """, (uid,))
        reviews = cursor.fetchall()
        cursor.close()
        conn.close()

         
        reviews_frame = tk.Frame(main_frame, bg="#22A298")
        reviews_frame.pack(fill="both", expand=True, pady=10)

        if reviews:
            canvas = tk.Canvas(reviews_frame, bg="#22A298")
            scrollbar = ttk.Scrollbar(reviews_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#22A298")

            for review_text, event_name in reviews:
                review_box = tk.Frame(scrollable_frame, bg="#E8F6F3", relief="raised", bd=1)
                review_box.pack(fill="x", padx=5, pady=5)
                tk.Label(review_box,
                        text=f"Εκδήλωση: {event_name}\nΚριτική: {review_text}",
                        bg="#E8F6F3",
                        wraplength=600,
                        justify="left").pack(pady=5)

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            scrollable_frame.bind("<Configure>", 
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
        else:
            tk.Label(reviews_frame,
                    text="Δεν έχετε καταχωρήσει ακόμη κριτικές",
                    font=("Times", 14),
                    bg="#22A298").pack(pady=20)

         
        tk.Button(main_frame,
                 text="Νέα Κριτική",
                 font=("Times", 12, "bold"),
                 bg="#DDB0B0",
                 width=20,
                 command=lambda: show_category_selection()).pack(pady=20)

    def show_category_selection():
         
        for widget in main_frame.winfo_children():
            widget.destroy()

        tk.Label(main_frame,
                text="Διαθέσιμες Εκδηλώσεις",
                font=("Times", 20, "bold"),
                bg="#22A298").pack(pady=10)

         
        conn, cursor = connect_to_mysql()
        cursor.execute("""
            SELECT eventID, name, datetime
            FROM events
            ORDER BY datetime DESC
        """)
        events = cursor.fetchall()
        cursor.close()
        conn.close()

        if not events:
            tk.Label(main_frame,
                    text="Δεν υπάρχουν διαθέσιμες εκδηλώσεις",
                    font=("Times", 14),
                    bg="#22A298").pack(pady=20)
            tk.Button(main_frame,
                     text="Πίσω",
                     font=("Times", 12),
                     bg="#DDB0B0",
                     command=show_previous_reviews).pack(pady=10)
            return

        events_frame = tk.Frame(main_frame, bg="#22A298")
        events_frame.pack(fill="both", expand=True, pady=10)

         
        canvas = tk.Canvas(events_frame, bg="#22A298")
        scrollbar = ttk.Scrollbar(events_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#22A298")

        for event_id, name, date in events:
            event_box = tk.Frame(scrollable_frame, bg="#E8F6F3", relief="raised", bd=1)
            event_box.pack(fill="x", padx=5, pady=5)
            tk.Label(event_box,
                    text=f"{name}\nΗμερομηνία: {date}",
                    bg="#E8F6F3",
                    wraplength=600,
                    justify="left").pack(side="left", pady=5, padx=5)
            tk.Button(event_box,
                     text="Προσθήκη Κριτικής",
                     bg="#DDB0B0",
                     command=lambda eid=event_id, ename=name: show_review_form(eid, ename)).pack(side="right", pady=5, padx=5)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scrollable_frame.bind("<Configure>", 
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

         
        tk.Button(main_frame,
                 text="Πίσω",
                 font=("Times", 12),
                 bg="#DDB0B0",
                 command=show_previous_reviews).pack(pady=10)

    def show_review_form(event_id, event_name):
        for widget in main_frame.winfo_children():
            widget.destroy()

        tk.Label(main_frame,
                 text=f"Γράψτε την κριτική σας για: {event_name}",
                 font=("Times", 20, "bold"),
                 bg="#22A298").pack(pady=10)

        review_frame = tk.Frame(main_frame, bg="#22A298")
        review_frame.pack(fill="both", expand=True, pady=10)

        review_text = tk.Text(review_frame,
                              width=60,
                              height=10,
                              wrap="word",
                              font=("Times", 12))
        review_text.pack(pady=10)

        word_count_lbl = tk.Label(review_frame,
                                  text="0/250 λέξεις",
                                  bg="#22A298")
        word_count_lbl.pack()

        def update_word_count(event=None):
            content = review_text.get("1.0", "end-1c").strip()
            words = content.split()
            count = len(words)
            word_count_lbl.config(text=f"{count}/250 λέξεις")

        review_text.bind("<KeyRelease>", update_word_count)

        msg_label = tk.Label(review_frame,
                             text="",
                             fg="red",
                             bg="#22A298")
        msg_label.pack(pady=5)

        def submit_review():
            content = review_text.get("1.0", "end-1c").strip()
            word_count = len(content.split())

            if word_count > 250:
                msg_label.config(
                    text="Η κριτική δεν μπορεί να υπερβαίνει τις 250 λέξεις.",
                    fg="red"
                )
                review_text.focus_set()
                return

            try:
                conn, cursor = connect_to_mysql()
                cursor.execute("""
                    INSERT INTO review (client_id, event_id, content, date)
                    VALUES (%s, %s, %s, CURDATE())
                """, (uid, event_id, content))
                conn.commit()
                cursor.close()
                conn.close()

                msg_label.config(text="Η κριτική καταχωρήθηκε επιτυχώς!", fg="green")
                window.after(1500, show_previous_reviews)

            except Exception as e:
                msg_label.config(text=f"Σφάλμα κατά την αποθήκευση: {str(e)}", fg="red")

        buttons_frame = tk.Frame(main_frame, bg="#22A298")
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame,
                  text="Υποβολή Κριτικής",
                  font=("Times", 12, "bold"),
                  bg="#DDB0B0",
                  width=20,
                  command=submit_review).pack(side="left", padx=5)

        tk.Button(buttons_frame,
                  text="Ακύρωση",
                  font=("Times", 12),
                  bg="#DDB0B0",
                  width=20,
                  command=show_previous_reviews).pack(side="left", padx=5)

     
    show_previous_reviews()

    if not parent:
        window.mainloop()

if __name__ == "__main__":
    show_reviews_screen()
