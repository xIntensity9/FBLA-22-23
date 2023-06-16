# Import the required modules
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import random as rand
from PIL import ImageTk, Image
import pymongo
from pymongo import MongoClient
import pyglet
import datetime


pyglet.font.add_file("./assets/Quicksand-Bold.ttf")

#uicksand = pyglet.font.load('Quicksand-Bold.ttf', bold=True)

cluster = MongoClient("mongodb+srv://RRHSfbla2023:IheBcYm1ZbOEephx@fbla2023project.wdozi9i.mongodb.net/?retryWrites=true&w=majority")
db = cluster["RRHSfbla2023"]
student_info = db["student_info"]
event_info = db["event_info"]
login_info = db["login_info"]

from about import about
from event import event
from register import register
from popups import error
from add_student import add_student

#from newStudent import inputStudent
#from report import report
#from winner import pickWinner
#from helper import open_help_window

#creates the home GUI
root = tk.Tk()
root.geometry("1000x500")
root.configure(bg='#1c1c1c')
default_font = ctk.CTkFont(size= 18, family= 'Roboto')
large_font = ctk.CTkFont(size= 25, family= 'Roboto')

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", fieldbackground= "#1c1c1c", background = "#1c1c1c", foreground= "white", font= ("none", 10), rowheight= 40, highlightbackground = "#1c1c1c", highlightcolor= "#1c1c1c")
style.configure("Treeview.Heading", background = "#1c1c1c", foreground= "white", borderwidth= 0)

root1 = tk.Toplevel()
root1.geometry("1000x500")
root1.configure(bg= '#1c1c1c')
students = student_info.find()

listbox = ttk.Treeview(root1, selectmode="extended",columns=("c1", "c2", "c3", "c4", "c5"),show="headings", height= 10)
listbox.column("# 1", anchor=CENTER, width = 199)
listbox.heading("# 1", text="Student id")
listbox.column("# 2", anchor=CENTER, width = 199)
listbox.heading("# 2", text="First Name")
listbox.column("# 3", anchor=CENTER, width = 199)
listbox.heading("# 3", text="Last Name")
listbox.column("# 4", anchor=CENTER, width = 199)
listbox.heading("# 4", text="Grade Level")
listbox.column("# 5", anchor=CENTER, width = 199)
listbox.heading("# 5", text="Points")

def refresh():
    for item in listbox.get_children():
        listbox.delete(item)
    students= student_info.find()
    count = 0
    for student in students:
        listbox.insert(parent='', index='end', text= "", iid= count, values= (student["_id"], student["first_name"], student["last_name"], student["grade"], student["point"]) )
        count+= 1
    listbox.place(relx= 0, rely= 0, anchor= "nw")

refresh()

def remove_student():
    item = listbox.selection()
    selection = listbox.item(item, option="values")
    temp = student_info.find()
    for student in temp:
        if int(student["_id"]) == int(selection[0]):
            print(student_info.delete_one({"_id": student["_id"]}))
    refresh()

def edit_student():
    item = listbox.selection()
    selection = listbox.item(item, option="values")

    edit_student_window = tk.Toplevel()
    edit_student_window.geometry("400x600")
    edit_student_window.configure(bg= '#1c1c1c')

    first_entry = ctk.CTkEntry(edit_student_window, bg_color= "#1C1F1F", border_width= 0, width= 200, font= ("Quicksand_bold", 15, "bold"))
    first_entry.insert(0, selection[1])
    def first_select(event):
        first_entry.select_range(0, END)
    first_entry.bind("<FocusIn>", first_select)
    first_entry.place(relx= 0.5, rely= 0.2, anchor= "center")

    last_entry = ctk.CTkEntry(edit_student_window, bg_color= "#1C1F1F", border_width= 0, width= 200, font= ("Quicksand_bold", 15, "bold"))
    last_entry.insert(0, selection[2])
    def last_select(event):
        last_entry.select_range(0, END)
    last_entry.bind("<FocusIn>", last_select)
    last_entry.place(relx= 0.5, rely= 0.4, anchor= "center")

    grade_entry = ctk.CTkEntry(edit_student_window, bg_color= "#1C1F1F", border_width= 0, width= 200, font= ("Quicksand_bold", 15, "bold"))
    grade_entry.insert(0, selection[3])
    def grade_select(event):
        grade_entry.select_range(0, END)
    grade_entry.bind("<FocusIn>", grade_select)
    grade_entry.place(relx= 0.5, rely= 0.6, anchor= "center")

    def get_submit():

        first= first_entry.get()
        last= last_entry.get()
        grade= grade_entry.get()
        student_info.update_one({"_id": int(selection[0])}, {"$set":{"first_name": str(first).capitalize(), "last_name": (str(last).capitalize()), "grade": int(grade)}})

        refresh()
        edit_student_window.destroy()

    submit_button = tk.Button(edit_student_window, text= "submit", command= get_submit)
    submit_button.place(relx= 0.5, rely= 0.8, anchor= "center")

edit_student_image = Image.open("./assets/edit_student.png")
edit_student_image = edit_student_image.resize((150, 45))
edit_student_image = ImageTk.PhotoImage(edit_student_image)
edit_button = tk.Button(root1, command= edit_student, image= edit_student_image, borderwidth= 0)
edit_button.place(relx= 0.15, rely= 0.875, anchor= "nw")

remove_student_image = Image.open("./assets/remove_student.png")
remove_student_image = remove_student_image.resize((150, 45))
remove_student_image = ImageTk.PhotoImage(remove_student_image)
remove_button = tk.Button(root1, command= remove_student, image= remove_student_image, borderwidth= 0)
remove_button.place(relx= 0.44, rely= 0.875, anchor= "nw")

save_exit_image = Image.open("./assets/save_exit.png")
save_exit_image = save_exit_image.resize((150, 45))
save_exit_image = ImageTk.PhotoImage(save_exit_image)
quit_button = tk.Button(root1, command= root1.withdraw, borderwidth= 0, image= save_exit_image)
quit_button.place(relx= 0.85, rely= 0.875, anchor= "ne")

root1.withdraw()

"""
#creates a label for the home GUI called Student Involment Tracker
left_frame = Frame(root, width = 275, height = 1000, bg= '#242424')
left_frame.place(x = 0, y= 0, anchor = NW)

top_frame = Frame(root, width = 2000, height = 100, bg= '#1c1c1c')
top_frame.place(x = 275, y= 0, anchor = NW)
"""

"""help_image = PhotoImage(file = "./assets/help_image.png")
help2_image = PhotoImage(file = "./assets/help2_image.png")"""
# Open and resize the image
img = Image.open("./assets/logo.png")
img = img.resize((400, 400))
img = ImageTk.PhotoImage(img)

# Create a label to display the image
label = tk.Label(root, image=img)

# Position the label in the center of the window
label.place(relx=0.5, rely=0.5, anchor="center")


"""
# Add a "Edit Student" button to the dialog box
edit_button = ctk.CTkButton(root, text="Edit Student", command=edit_student)
edit_button.place(relx= .225, rely= .8, height= 35, width = 200)"""
"""
# Add a "remove student" button to the dialog box
remove_button = ctk.CTkButton(root, text="Remove student", command= remove_student)
remove_button.place(relx= .425, rely= .8, height= 35, width = 200)"""
"""
# Add a "Edit student points" button to the dialog box
add_points_button = ctk.CTkButton(root, text= "Edit student points", command= add_points)
add_points_button.place(relx= .625, rely= .8, height= 35, width = 200)"""
"""
# Add a "remove all" button to the dialog box
remove_all = ctk.CTkButton(root, text="Remove all", command= remove_everyone)
remove_all.place(relx= .825, rely= .8, height= 35, width = 200)"""

"""
enter = ctk.CTkButton(root, text= "Enter", command= get_entry)
enter.place(relx = .775, rely= .65, height= 25, width= 120, anchor= CENTER)"""
"""
clear = ctk.CTkButton(root, text= "Clear", command= clear)
clear.place(relx = .375, rely= .65, height= 25, width= 120, anchor= CENTER)"""

"""
help_button = tk.Button(root, image= help_image,command=open_help_window, bg="#1c1c1c", fg= "#9b9a92", font= large_font, bd = 0, anchor = "w")
help_button.place(x= 1800, y= 25, anchor=NW)
help_frame = Frame(root, width = 500, height = 900, bg= '#242424')"""
"""
# Allows you to add new students to the database
add_student = tk.Button(root, text="Add new student",command=inputStudent, width=22, bg="#242424", fg= "#9b9a92", font= default_font, bd = 0, anchor = "w")
add_student.place(x= 30, y= 50, anchor=NW)
"""
"""
# Creates a report of the entire database
winner_button = tk.Button(root, text="Pick Winner", command=pickWinner, width=22, bg="#242424", fg= "#9b9a92", font= default_font, bd = 0, anchor= "w")
winner_button.place(x= 30, y= 150, anchor=NW)"""
"""
# Creates a report of the entire database
report_button = tk.Button(root, text="Create Report", command=report, width=22, bg="#242424", fg= "#9b9a92", font= default_font, bd = 0, anchor= "w")
report_button.place(x= 30, y= 250, anchor=NW)
"""

""" 
LEFT SIDE 
"""


"""
RIGHT SIDE

button = tk.Button(root, text="     About Us", command=root.destroy, width=25, bg="#242424", fg= "#9b9a92", font= default_font, bd = 0, anchor= "w")
button.place(relx=0.85,rely=0.1, anchor="center")

button = tk.Button(root, text="     Placeholder", command=root.destroy, width=25, bg="#242424", fg= "#9b9a92", font= default_font, bd = 0, anchor= "w")
button.place(relx=0.85,rely=0.25, anchor="center")

button = tk.Button(root, text="     Placeholder", command=root.destroy, width=25, bg="#242424", fg= "#9b9a92", font= default_font, bd = 0, anchor= "w")
button.place(relx=0.85,rely=0.4, anchor="center")
"""

## IMAGE BUTTONS

event_image = Image.open("./assets/event.png")
event_image = event_image.resize((250, 75))
event_image = ImageTk.PhotoImage(event_image)
event_button = tk.Button(root, image=event_image, command= event)
event_button.place(relx=0.85, rely=0.2, anchor="center")

add_student_image = Image.open("./assets/add_student.png")
add_student_image = add_student_image.resize((250, 75))
add_student_image = ImageTk.PhotoImage(add_student_image)
add_student_button = tk.Button(root, image=add_student_image, command= add_student)
add_student_button.place(relx=0.15, rely=0.2, anchor="center")

about_image = Image.open("./assets/about.png")
about_image = about_image.resize((250, 75))
about_image = ImageTk.PhotoImage(about_image)
about_button = tk.Button(root, image=about_image, command=about)
about_button.place(relx=0.85, rely=0.4, anchor="center")

view_image = Image.open("./assets/view_entries.png")
view_image = view_image.resize((250, 75))
view_image = ImageTk.PhotoImage(view_image)
view_button = tk.Button(root, image=view_image, command= root1.deiconify) # CHANGE THIS
view_button.place(relx=0.85, rely=0.6, anchor="center")

help_image = Image.open("./assets/help.png")
help_image = help_image.resize((250, 75))
help_image = ImageTk.PhotoImage(help_image)
help_button = tk.Button(root, image=help_image, command=about) # CHANGE THIS
help_button.place(relx=0.85, rely=0.8, anchor="center")

upcoming_event_image = Image.open("./assets/upcoming_events.png")
upcoming_event_image = upcoming_event_image.resize((270, 75))
upcoming_event_image = ImageTk.PhotoImage(upcoming_event_image)
upcoming_event = Label(root, image= upcoming_event_image, bd= 0)
upcoming_event.place(relx= .5, rely= .1, anchor= CENTER)


login_screen = Frame(root, width= 1000, height= 500, bg= '#1c1c1c')
login_screen.place(relx= 0, rely= 0, anchor= NW)

sign_in_image = Image.open("./assets/sign_in.png")
sign_in_image = sign_in_image.resize((270, 68))
sign_in_image = ImageTk.PhotoImage(sign_in_image)
sign_in = Label(login_screen, image= sign_in_image, bd= 0)
sign_in.place(relx= .5, rely= .35, anchor= CENTER)

username_entry = ctk.CTkEntry(login_screen, bg_color= "#1C1F1F", border_width= 0, width= 200, font= ("Quicksand_bold", 15, "bold"), placeholder_text= "username")
username_entry.place(relx= .5, rely= .5, anchor= CENTER)

password_entry = ctk.CTkEntry(login_screen, bg_color= "#1C1F1F", border_width= 0, width= 200, font= ("Quicksand_bold", 15, "bold"), placeholder_text= "password", show= '*')
password_entry.place(relx= .5, rely= .65, anchor= CENTER)

box_image = Image.open("./assets/box.png")
box_image = box_image.resize((250, 250))
box_image = ImageTk.PhotoImage(box_image)

first_box = tk.Label(image= box_image, borderwidth= 0)
second_box = tk.Label(image= box_image, borderwidth= 0)
third_box = tk.Label(image= box_image, borderwidth= 0)

def login():
    temp = student_info.find()
    temp2 = login_info.find()
    logged_in = False

    if logged_in == False:
        for item in temp:
            if str(password_entry.get()) == str(item["_id"]) and str(username_entry.get()) == str(item["last_name"]):
                event_button.destroy()
                add_student_button.destroy()
                view_button.destroy()
                login_screen.place_forget()
                label.destroy()
                logged_in = True

                sign_out.place(relx=0.15, rely=0.8, anchor="center")
                help_button.place(relx= 0.5, rely= 0.8, anchor= "center")
                about_button.place(relx= 0.85, rely= 0.8, anchor= "center")
                upcoming_event.place(relx= .5, rely= .08, anchor= CENTER)

                first_box.place(relx= 0.2, rely= 0.4, anchor= "center")

                second_box.place(relx= 0.5, rely= 0.4, anchor= "center")

                third_box.place(relx= 0.8, rely= 0.4, anchor= "center")

    if logged_in == False:
        for item2 in temp2:
            if str(password_entry.get()) == str(item2["password"]) and str(username_entry.get()) == str(item2["username"]):
                login_screen.place_forget()
                sign_out.place(relx=0.15, rely=0.4, anchor="center")
                logged_in = True

                upcoming_event.place_forget()

    if logged_in == False:
        if str(password_entry.get()) == "" or str(username_entry.get()) == "":
            error("Please fill out all the fields.")
        else:
            error("Incorrect username or password.")
    

login_image = Image.open("./assets/login.png")
login_image = login_image.resize((60, 60))
login_image = ImageTk.PhotoImage(login_image)
login_button = tk.Button(login_screen, image=login_image, command=login) # CHANGE THIS
login_button.place(relx=0.425, rely=0.8, anchor="center")

register_image = Image.open("./assets/register.png")
register_image = register_image.resize((60, 60))
register_image = ImageTk.PhotoImage(register_image)
register_button = tk.Button(login_screen, image=register_image, command=register) # CHANGE THIS
register_button.place(relx=0.575, rely=0.8, anchor="center")

img1 = Image.open("./assets/logo.png")
img1 = img1.resize((200, 200))
img1 = ImageTk.PhotoImage(img1)


def place_login_frame():
    login_screen.place(relx= 0, rely= 0, anchor= NW)
    sign_out.place_forget()
    username_entry.delete(0, END)
    password_entry.delete(0, END)

sign_out_image = Image.open("./assets/sign_out.png")
sign_out_image = sign_out_image.resize((250, 75))
sign_out_image = ImageTk.PhotoImage(sign_out_image)
sign_out = tk.Button(root, image=sign_out_image, command= place_login_frame)



# keeps gui running
if __name__ == "__main__":
    root.mainloop()
