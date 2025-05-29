import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import simpledialog
from models.friends import FriendsSystem

class FriendsPage(tk.Frame):
    def __init__(self, parent, friends_system, current_user):
        super().__init__(parent, bg="#22A298")        
        self.fs = friends_system
        self.current_user = current_user

        self.tab_container = tk.Frame(self, bg="#22A298")
        self.tab_container.pack(fill=tk.BOTH, expand=True)

        self.setup_tabs()

    def setup_tabs(self):
        tabs_frame = tk.Frame(self, bg="#22A298")
        tabs_frame.pack(fill=tk.X)

        tk.Button(tabs_frame, text="Search", command=self.show_search).pack(side=tk.LEFT)
        tk.Button(tabs_frame, text="Friends", command=self.show_friends).pack(side=tk.LEFT)
        tk.Button(tabs_frame, text="Pending", command=self.show_pending).pack(side=tk.LEFT)

        self.search_frame = tk.Frame(self.tab_container, bg="#22A298")
        self.friends_frame = tk.Frame(self.tab_container, bg="#22A298")
        self.pending_frame = tk.Frame(self.tab_container, bg="#22A298")

        self.setup_search()
        self.setup_friends()
        self.setup_pending()

        self.show_search()

    def setup_search(self):
        tk.Label(self.search_frame, text="Search Users:", bg="#22A298").pack()
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack()
        tk.Button(self.search_frame, text="Search", command=self.search_users).pack()

        self.search_results = tk.Frame(self.search_frame, bg="white")
        self.search_results.pack(fill=tk.BOTH, expand=True)

    def setup_friends(self):
        tk.Label(self.friends_frame, text="Your Friends:", bg="white").pack()
        self.friends_list = tk.Frame(self.friends_frame, bg="white")
        self.friends_list.pack(fill=tk.BOTH, expand=True)

    def setup_pending(self):
        tk.Label(self.pending_frame, text="Pending Requests:", bg="white").pack()
        self.pending_list = tk.Frame(self.pending_frame, bg="white")
        self.pending_list.pack(fill=tk.BOTH, expand=True)

    def show_search(self):
        self.clear_tabs()
        self.search_frame.pack(fill=tk.BOTH, expand=True)

    def show_friends(self):
        self.clear_tabs()
        self.friends_frame.pack(fill=tk.BOTH, expand=True)
        self.refresh_friends()

    def show_pending(self):
        self.clear_tabs()
        self.pending_frame.pack(fill=tk.BOTH, expand=True)
        self.refresh_pending()

    def clear_tabs(self):
        self.search_frame.pack_forget()
        self.friends_frame.pack_forget()
        self.pending_frame.pack_forget()

    def search_users(self):
        for w in self.search_results.winfo_children():
            w.destroy()
        query = self.search_entry.get()
        if not query:
            messagebox.showwarning("Input", "Search User!")
            return
        self.fs.cursor.execute("SELECT user_id, username FROM users WHERE username LIKE %s", (f"%{query}%",))
        results = self.fs.cursor.fetchall()
        for user_id, username in results:
            if user_id == self.current_user:
                continue
            f = tk.Frame(self.search_results, bg="white")
            f.pack(fill=tk.X)
            tk.Label(f, text=f"{username} (ID: {user_id})", bg="white").pack(side=tk.LEFT)
            tk.Button(f,
                       text="Add",
                       font=("Times", 14),
                       bg="#DDB0B0",
                       fg="black",
                       width=20,
                       command=lambda uid=user_id: self.send_request(uid)
                      ).pack(side=tk.RIGHT, padx=5, pady=5)
    def send_request(self, uid):
        try:
            self.fs.send_friend_request(self.current_user, uid)
            messagebox.showinfo("Sent", "Request sent!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_friends(self):
        for w in self.friends_list.winfo_children():
            w.destroy()
        friends = self.fs.get_friends(self.current_user)
        for user_id, username in friends:
            tk.Label(self.friends_list, text=f"{username} (ID: {user_id})", bg="white").pack(anchor='w')

    def refresh_pending(self):
        for w in self.pending_list.winfo_children():
            w.destroy()
        pending = self.fs.get_pending_requests(self.current_user)
        for sid, rid, uname in pending:
            f = tk.Frame(self.pending_list, bg="white")
            f.pack(fill=tk.X)
            if sid == self.current_user:
                tk.Label(f, text=f"You sent request to {uname}", bg="white").pack(side=tk.LEFT)
            else:
                tk.Label(f, text=f"{uname} sent you a request", bg="white").pack(side=tk.LEFT)
                tk.Button(f,
                           text="Accept",
                           font=("Times", 14),
                           bg="#DDB0B0",
                           fg="black",
                           width=20,
                            command=lambda s=sid, r=rid: self.respond(s, r, "accepted")
                          ).pack(side=tk.RIGHT, padx=5, pady=5)                

                tk.Button(f,
                           text="Accept",
                           font=("Times", 14),
                           bg="#DDB0B0",
                           fg="black",
                           width=20,
                            command=lambda s=sid, r=rid: self.respond(s, r, "rejected")
                          ).pack(side=tk.RIGHT, padx=5, pady=5)             
                

    def respond(self, sender_id, receiver_id, status):
        try:
            self.fs.update_friend_request_status(sender_id, receiver_id, status)
            self.refresh_pending()
        except Exception as e:
            messagebox.showerror("Error", str(e))

