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

cluster = MongoClient("mongodb+srv://RRHSfbla2023:IheBcYm1ZbOEephx@fbla2023project.wdozi9i.mongodb.net/?retryWrites=true&w=majority")
db = cluster["RRHSfbla2023"]
student_info = db["student_info"]

def view_entries():
    root = tk.Tk()
    root.geometry("1000x500")
    root.configure(bg= '#1c1c1c')
    students = student_info.find()

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", fieldbackground= "#1c1c1c", background = "#1c1c1c", foreground= "#9b9a92")
    
    listbox = ttk.Treeview(root, selectmode="extended",columns=("c1", "c2", "c3", "c4", "c5"),show="headings", height= 12)
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

    count = 0
    for student in students:
        listbox.insert(parent='', index='end', text= "", iid= count, values= (student["_id"], student["first_name"], student["last_name"], student["grade"], student["point"]) )
        count+= 1
    listbox.place(relx= 0, rely= 0, anchor= "nw")

