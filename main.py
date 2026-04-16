from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json


# ---------------------------- CONSTANTS ------------------------------- #


LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
EMAIL = "example@gmail.com"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = [choice(LETTERS) for _ in range(randint(8, 10))]
    numbers = [choice(NUMBERS) for _ in range(randint(2, 4))]
    symbols = [choice(SYMBOLS) for _ in range(randint(2, 4))]
    password_list = letters + numbers + symbols
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)


# ---------------------------- SEARCH PASSWORD ------------------------------- #


def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data:
            data_dict = json.load(data)
            email = data_dict[website]["email"]
            password = data_dict[website]["password"]
    except KeyError, FileNotFoundError:
        messagebox.showerror(title="Error", message=f"You don't have a password for {website}.")
    else:
        messagebox.showinfo(title=f"{website} Info", message=f"Email/Username:\n{email}\n\nPassword:\n{password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) < 1 or len(email) < 1 or len(password) < 1:
        messagebox.showerror(title="Error", message="Please fill out all fields.")
    else:
        try:
            with open("data.json", "r") as data:
                # reading old data
                current_data = json.load(data)

        except FileNotFoundError:
            with open("data.json", "w") as data:
                json.dump(new_data, data, indent=4)

        else:
            # updating old data with new data
            current_data.update(new_data)
            with open("data.json", "w") as data:
                json.dump(current_data, data, indent=4)

        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


# window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# canvas (logo)
canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)


# labels
website_label = Label(text="Website:", font=("Arial", 10))
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", font=("Arial", 10))
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=("Arial", 10))
password_label.grid(column=0, row=3)


# entries
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=51)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, EMAIL)
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)


# buttons
generate_button = Button(text="Generate Password", font=("Arial", 8), command=generate_password)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", font=("Arial", 8), width=50, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", font=("Arial", 8), width=16, command=find_password)
search_button.grid(column=2, row=1)


window.mainloop()

