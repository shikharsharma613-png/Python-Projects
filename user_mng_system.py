import tkinter as tk
from tkinter import messagebox, ttk
import pyodbc 
import re

# ---------- DATABASE CONNECTION ----------
def get_connection():

    return pyodbc.connect(
        'Driver={SQL Server};'
        'Server=THINKBOOK\\SQLEXPRESS;'   
        'Database=maindb;'                  
        'Trusted_Connection=yes;'
    )

# ---------- INITIALIZE DATABASE ----------
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
        CREATE TABLE users (
            id INT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(100),
            gender VARCHAR(20),
            phone CHAR(10) CHECK (phone NOT LIKE '%[^0-9]%' AND LEN(phone) = 10),
            email VARCHAR(100),
            qualification VARCHAR(50)
        )
    """)
    conn.commit()
    conn.close()

# ---------- REGISTRATION WINDOW ----------
def open_registration():
    reg = tk.Toplevel(root)
    reg.title("User Registration Form")
    reg.geometry("500x500")
    reg.transient(root)
    reg.grab_set() 

    username = tk.StringVar()
    password = tk.StringVar()
    gender = tk.StringVar(value=" ")
    phone = tk.StringVar()
    email = tk.StringVar()
    qualification = tk.StringVar()

    def save_data():
        uname = username.get()
        pwd = password.get()
        gen = gender.get()
        ph = phone.get()
        em = email.get()
        qual = qualification.get()

        if not uname or not pwd or not gen or not ph or not em or not qual:
            messagebox.showerror("Error", "All fields are required!")
            return
        if not ph.isdigit() or len(ph) != 10:
            messagebox.showerror("Error", "Invalid phone number! Enter a 10-digit number.")
            return
        
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, em):
            messagebox.showerror("Error", "Invalid email format! Example: user@example.com")
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, gender, phone, email, qualification)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (uname, pwd, gen, ph, em, qual))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User Registered Successfully!")
            reset_form()
        except pyodbc.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reset_form():
        username.set("")
        password.set("")
        gender.set(value=" ")
        phone.set("")
        email.set("")
        qualification.set("")

    tk.Label(reg, text="User Name").grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Entry(reg, textvariable=username, width=30).grid(row=0, column=1, pady=5)

    tk.Label(reg, text="Password").grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Entry(reg, textvariable=password, show='*', width=30).grid(row=1, column=1, pady=5)

    tk.Label(reg, text="Gender").grid(row=2, column=0, padx=10, pady=10, sticky='w')
    tk.Radiobutton(reg, text="Male", variable=gender, value="Male").grid(row=2, column=1, sticky='w')
    tk.Radiobutton(reg, text="Female", variable=gender, value="Female").grid(row=2, column=1, sticky='e')

    tk.Label(reg, text="Phone Number").grid(row=3, column=0, padx=10, pady=10, sticky='w')
    tk.Entry(reg, textvariable=phone, width=30).grid(row=3, column=1, pady=5)

    tk.Label(reg, text="E-Mail Address").grid(row=4, column=0, padx=10, pady=10, sticky='w')
    tk.Entry(reg, textvariable=email, width=30).grid(row=4, column=1, pady=5)

    tk.Label(reg, text="Qualification").grid(row=5, column=0, padx=10, pady=10, sticky='w')
    combo = ttk.Combobox(reg, textvariable=qualification, width=27, state="readonly")
    combo['values'] = ("10th", "12th", "Graduate", "Post-Graduate", "PhD")
    combo.grid(row=5, column=1, pady=5)

    tk.Button(reg, text="Save", width=10, command=save_data, bg="lightgreen").grid(row=6, column=0, pady=20)
    tk.Button(reg, text="Reset", width=10, command=reset_form, bg="lightgrey").grid(row=6, column=1, pady=20)

# ---------- CRUD WINDOW ----------
def open_crud():
    crud = tk.Toplevel(root)
    crud.title("CRUD Operations")
    crud.geometry("500x400")
    crud.transient(root)
    crud.grab_set() 


    search_name = tk.StringVar()

    tk.Label(crud, text="User Name").grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(crud, textvariable=search_name, width=25).grid(row=0, column=1, pady=10)

    result_box = tk.Text(crud, width=55, height=12)
    result_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def search_user():
        uname = search_name.get()
        if not uname :
            messagebox.showerror("Error", "Please enter a username to search!")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (uname,))
        row = cursor.fetchone()
        conn.close()

        result_box.delete(1.0, tk.END)
        if row:
            result_box.insert(tk.END, f"Username: {row[1]}\nPassword: {row[2]}\n"
                                      f"Gender: {row[3]}\nPhone: {row[4]}\nEmail: {row[5]}\n"
                                      f"Qualification: {row[6]}")
        else:
            result_box.insert(tk.END, "No user found.")

    def update_user():
        uname = search_name.get()
        if not uname:
            messagebox.showerror("Error", "Enter a username to update!")
            return

        update_window = tk.Toplevel(crud)
        update_window.title("Update User")
        update_window.geometry("400x400")

        password = tk.StringVar()
        gender = tk.StringVar()
        phone = tk.StringVar()
        email = tk.StringVar()
        qualification = tk.StringVar()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (uname,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            messagebox.showerror("Error", "User not found!")
            update_window.destroy()
            return

        password.set(row[2])
        gender.set(row[3])
        phone.set(row[4])
        email.set(row[5])
        qualification.set(row[6])

        tk.Label(update_window, text="Password").grid(row=0, column=0, pady=10)
        tk.Entry(update_window, textvariable=password, width=30).grid(row=0, column=1)

        tk.Label(update_window, text="Gender").grid(row=1, column=0, pady=10)
        tk.Radiobutton(update_window, text="Male", variable=gender, value="Male").grid(row=1, column=1, sticky='w')
        tk.Radiobutton(update_window, text="Female", variable=gender, value="Female").grid(row=1, column=1, sticky='e')

        tk.Label(update_window, text="Phone").grid(row=2, column=0, pady=10)
        tk.Entry(update_window, textvariable=phone, width=30).grid(row=2, column=1)

        tk.Label(update_window, text="Email").grid(row=3, column=0, pady=10)
        tk.Entry(update_window, textvariable=email, width=30).grid(row=3, column=1)

        tk.Label(update_window, text="Qualification").grid(row=4, column=0, pady=10)
        combo = ttk.Combobox(update_window, textvariable=qualification, width=27, state="readonly")
        combo['values'] = ("10th", "12th", "Graduate", "Post-Graduate", "PhD")
        combo.grid(row=4, column=1, pady=5)

        def save_update():
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET password=?, gender=?, phone=?, email=?, qualification=?
                WHERE username=?
            """, (password.get(), gender.get(), phone.get(), email.get(), qualification.get(), uname))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "User updated successfully!")
            update_window.destroy()

        tk.Button(update_window, text="Save", command=save_update, bg="lightgreen").grid(row=5, column=1, pady=20)

    def delete_user():
        uname = search_name.get()
        if not uname:
            messagebox.showerror("Error", "Enter a username to delete!")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (uname,))
        conn.commit()
        conn.close()
        result_box.delete(1.0, tk.END)
        messagebox.showinfo("Deleted", "User deleted successfully!")

    def reset_search():
        search_name.set("")
        result_box.delete(1.0, tk.END)

    tk.Button(crud, text="Search", width=10, command=search_user, bg="lightblue").grid(row=0, column=2, padx=10)
    tk.Button(crud, text="Update", width=10, command=update_user, bg="lightgreen").grid(row=3, column=0, pady=10)
    tk.Button(crud, text="Delete", width=10, command=delete_user, bg="red").grid(row=3, column=1, pady=10)
    tk.Button(crud, text="Reset", width=10, command=reset_search, bg="lightgrey").grid(row=3, column=2, pady=10)

# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Main Window")
root.geometry("400x200")

icon = tk.PhotoImage(file=r"C:\Users\shikh\OneDrive\图片\wp_pro.png")
root.iconphoto(False,icon)

init_db()

tk.Label(root, text="Main Menu", font=("Arial", 16, "bold")).pack(pady=20)
tk.Button(root, text="Registration", width=20, command=open_registration, bg="skyblue").pack(pady=10)
tk.Button(root, text="CRUD Operations", width=20, command=open_crud, bg="lightyellow").pack(pady=10)

root.mainloop()
