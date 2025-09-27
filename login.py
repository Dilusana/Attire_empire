import tkinter as tk
from tkinter import messagebox
import dashboard
import billingFrame
import datetime
def start_login():
    
    def login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "thushan" and password == "1234":
            root.destroy()
            dashboard.open_dashboard()
        elif username == "lakshi" and password == "1234":
            root.destroy()
            billingFrame.open_billing()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")




    root = tk.Tk()
    root.title("Login Page")
    root.geometry("400x400")
    root.configure(bg="#f0f0f0")
    
    def get_greeting():
        current_hour = datetime.datetime.now().hour
        if 5 <= current_hour < 12:
            return "Good Morning!"
        elif 12 <= current_hour < 17:
            return "Good Afternoon!"
        elif 17 <= current_hour < 21:
            return "Good Evening!"
        else:
            return "Welcome!"

    tk.Label(root, text=get_greeting(), font=("Arial", 20, "bold"), bg="white", fg="#333").pack(pady=(20, 5))
    

    tk.Label(root, text="Username", bg="#f0f0f0").pack(pady=(20, 5))
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password", bg="#f0f0f0").pack(pady=(10, 5))
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Button(root, text="Login", command=login, bg="#4CAF50", fg="white").pack(pady=20)

    root.mainloop()

