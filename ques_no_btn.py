import tkinter as tk
import random
from tkinter import messagebox


def show_message():
    messagebox.showinfo("Good","I knew it, I love you too ❤️")
    window.destroy()

def move_button(event):
    max_x = button_frame.winfo_width() - no_button.winfo_width()
    max_y = button_frame.winfo_height() - no_button.winfo_height()
    x = random.randint(0, max_x)
    y = random.randint(0, max_y)
    no_button.place(x=x, y=y)

window = tk.Tk()
window.title("question for you")
window.geometry("600x400")
window.resizable(False, False)

question_label = tk.Label(window, text="Do You Love Me?", font=("Arial", 20))
question_label.pack(pady=30)

button_frame = tk.Frame(window, width=500, height=150)
button_frame.pack(pady=20)
button_frame.pack_propagate(False)

yes_button = tk.Button(button_frame, text="YES", font=("Arial", 14), command=show_message)
yes_button.place(x=150, y=50)

no_button = tk.Button(button_frame, text="NO", font=("Arial", 14))
no_button.place(x=300, y=50)
no_button.bind("<Enter>", move_button)

response_label = tk.Label(window, text="", font=("Arial", 18))
response_label.pack(pady=30)

window.mainloop()
