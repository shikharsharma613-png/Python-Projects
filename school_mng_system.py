import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

window = tk.Tk()
window.geometry("1350x700")
window.title("Student Management System")

# Heading
tk.Label(window, text="Student Management System",
         font=("Times new roman", 35, "bold"),
         bg="blue", fg="yellow", bd=12, relief=tk.GROOVE
         ).pack(side=tk.TOP, fill=tk.X)

# Frames
Frame_Details = tk.LabelFrame(window, text="Enter details",
                             font=("Times new roman", 22, "bold"),
                             bd=12, relief=tk.GROOVE, bg="#e3f4f1")
Frame_Details.place(x=20, y=100, width=400, height=575)

Frame_Data = tk.Frame(window, bd=12, relief=tk.GROOVE, bg="#e3f4f1")
Frame_Data.place(x=440, y=100, width=890, height=575)

# Variables
rollno = tk.StringVar()
name = tk.StringVar()
email = tk.StringVar()
gender = tk.StringVar()
class_var = tk.StringVar()
contact = tk.StringVar()
dob = tk.StringVar()
address = tk.StringVar()

# ================= ENTRY FIELDS =================
labels = ["Name", "Roll No", "Email", "Gender", "Class", "Contact", "DOB", "Address"]
vars_ = [name, rollno, email, gender, class_var, contact, dob, address]

for i in range(len(labels)):
    tk.Label(Frame_Details, text=labels[i], font=("Times new roman", 17),
             bg="#e3f4f1").grid(row=i, column=0, padx=5, pady=5)
    tk.Entry(Frame_Details, textvariable=vars_[i],
             font=("Times new roman", 17), bd=5).grid(row=i, column=1, padx=5, pady=5)

# ================= DATABASE CONNECTION =================

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=THINKBOOK\\SQLEXPRESS;"   # change if needed
        "DATABASE=student_mng_system;"
        "Trusted_Connection=yes;"
    )

# ================= CRUD FUNCTIONS =================

def GET_DATA():
    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

    Student_table.delete(*Student_table.get_children())

    for row in rows:
        Student_table.insert('', tk.END, values=row)

    con.close()

def ADD_DATA():
    if rollno.get() == "" or name.get() == "" or class_var.get() == "":
        messagebox.showerror("Error", "All required fields must be filled")
        return

    con = get_connection()
    cur = con.cursor()

    cur.execute(
        "INSERT INTO students VALUES (?,?,?,?,?,?,?,?)",
        (rollno.get(), name.get(), email.get(), gender.get(),
         class_var.get(), contact.get(), dob.get(), address.get())
    )

    con.commit()
    con.close()

    GET_DATA()
    CLEAR()
    messagebox.showinfo("Success", "Record Added")

def UPDATE_DATA():
    con = get_connection()
    cur = con.cursor()

    cur.execute(
        """UPDATE students 
           SET name=?, email=?, gender=?, class=?, contact=?, dob=?, address=?
           WHERE rollno=?""",
        (name.get(), email.get(), gender.get(), class_var.get(),
         contact.get(), dob.get(), address.get(), rollno.get())
    )

    con.commit()
    con.close()

    GET_DATA()
    CLEAR()

def DELETE():
    con = get_connection()
    cur = con.cursor()

    cur.execute("DELETE FROM students WHERE rollno=?", (rollno.get(),))

    con.commit()
    con.close()

    GET_DATA()
    CLEAR()
    messagebox.showinfo("Deleted", "Record Deleted")

def CLEAR():
    rollno.set("")
    name.set("")
    email.set("")
    gender.set("")
    class_var.set("")
    contact.set("")
    dob.set("")
    address.set("")

def FOCUS(event):
    cursor = Student_table.focus()
    content = Student_table.item(cursor)
    row = content['values']

    if row:
        rollno.set(row[0])
        name.set(row[1])
        email.set(row[2])
        gender.set(row[3])
        class_var.set(row[4])
        contact.set(row[5])
        dob.set(row[6])
        address.set(row[7])

# ================= BUTTONS =================
Frame_Btn = tk.Frame(Frame_Details, bg="#e3f4f1", bd=7, relief=tk.GROOVE)
Frame_Btn.place(x=15, y=420, width=350, height=120)

tk.Button(Frame_Btn, text="Add", width=13, command=ADD_DATA).grid(row=0, column=0, padx=5, pady=5)
tk.Button(Frame_Btn, text="Delete", width=13, command=DELETE).grid(row=0, column=1, padx=5, pady=5)
tk.Button(Frame_Btn, text="Update", width=13, command=UPDATE_DATA).grid(row=1, column=0, padx=5, pady=5)
tk.Button(Frame_Btn, text="Clear", width=13, command=CLEAR).grid(row=1, column=1, padx=5, pady=5)

# ================= TABLE =================
Frame_Database = tk.Frame(Frame_Data, bd=11, relief=tk.GROOVE)
Frame_Database.pack(fill=tk.BOTH, expand=True)

scroll_x = tk.Scrollbar(Frame_Database, orient=tk.HORIZONTAL)
scroll_y = tk.Scrollbar(Frame_Database, orient=tk.VERTICAL)

Student_table = ttk.Treeview(Frame_Database,
    columns=("Roll No","Name","Email","Gender","Class","Contact","DOB","Address"),
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set)

scroll_x.config(command=Student_table.xview)
scroll_y.config(command=Student_table.yview)

scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

for col in Student_table["columns"]:
    Student_table.heading(col, text=col)
    Student_table.column(col, width=100)

Student_table["show"] = "headings"
Student_table.pack(fill=tk.BOTH, expand=True)

Student_table.bind("<ButtonRelease-1>", FOCUS)

GET_DATA()
window.mainloop()