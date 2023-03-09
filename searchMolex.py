# This program was made to search for test results of gateway with MAC address.
# The application has simple GUI. Results are presented in tabular.
# To see the results of the test, MAC address needs to be typed to the first label.


# Author: Kacper Kuczmarski 16.08.2022
# Consul: Mati
# Molex Connected Enterprise Solutions Sp. z o.o.

import csv
import glob
import os
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

# Index number of Table
indexNum = 0
# Initial value of folder path
folder_path = 'W:\MAC address test\\python'


def searchCoreSync():
    # Initialization of the window and main frame
    root = Tk()
    root.geometry("850x500")
    root.title("Mac Address search")
    root.configure(background='#3D3B3C')
    frm = ttk.Frame(root, padding=10)
    frm.grid()

    # Molex img
    #img = tkinter.PhotoImage(file="molex.png")
    #imgLabel = tkinter.Label(root, image=img)
    #imgLabel.place(relx=0.8, rely=0.1, anchor='center')

    # ==== TextBoxes ====

    # Text for access path (read only)
    textPath = Text(root, width=50, height=1)
    textPath.place(x=240, y=152)
    textPath.config(state='disabled')

    # Allow user to select a directory and store it in global var
    # called folder_path
    def browse_button():
        global folder_path
        folder_path = filedialog.askdirectory()
        defPath = StringVar(root, value=folder_path)
        path = Entry(root, textvariable=defPath, width=40).place(x=240, y=92)

    # Entry point for MAC address input
    macAddEntry = ttk.Entry(root, width=40)
    macAddEntry.place(x=240, y=32)
    # Path to test results
    defPath = StringVar(root, value=folder_path)
    path = Entry(root, textvariable=defPath, width=40).place(x=240, y=92)

    # ==== Main button (search) handle ====
    def findButtonHandle():
        global indexNum
        notFound = 0
        macAdd = macAddEntry.get()
        filename = ''
        # CSV part - searching for every *.csv file in the folder
        for filename in glob.glob(os.path.join(folder_path, '*.csv')):
            with open(os.path.join(os.getcwd(), filename), newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                # Reading data from *.csv file
                for row in reader:
                    try:
                        if macAdd != "" and macAdd in row['MAC Address']:
                            notFound = 0
                            # Scrolling results to the newest
                            list.yview_moveto(1)
                            # Increment by 1 index of the table
                            indexNum += 1
                            # Access path update
                            textPath.config(state='normal')
                            textPath.delete(1.0, END)
                            textPath.insert(1.0, filename)
                            textPath.config(state='disabled')
                            # Inserting data to the table
                            list.insert(parent='', index='end', iid=indexNum, text='',
                                        values=(macAdd, row['Time'], row['Date'], row['Model'], row['Worker ID'],
                                                row['Current'], row['Voltage'], row['Power'], row['COM Test']))
                            break
                        else:
                            notFound = 1
                    except:
                        notFound = 1
            if notFound == 0:
                tkinter.messagebox.showinfo(title="Searching", message="File found!")
                break

        if notFound == 1:
            tkinter.messagebox.showinfo(title="Searching", message="No file found matching MAC Address!")
        if filename == '':
            tkinter.messagebox.showinfo(title="Searching", message="No .csv file in this folder!")

    # ==== Labels ====
    label1 = ttk.Label(root, text="MAC Address: ", font=("Malgun Gothic Semilight", 17),background='#3D3B3C', foreground = '#E3E2DD').place(x=40, y=30)
    ttk.Label(root, text="File path: ", font=("Malgun Gothic Semilight", 17),background='#3D3B3C', foreground = '#E3E2DD').place(x=40, y=90)
    ttk.Label(root, text="Access path: ", font=("Malgun Gothic Semilight", 17),background='#3D3B3C', foreground = '#E3E2DD').place(x=40, y=150)
    space = ' '
    footerLabel = ttk.Label(root,text=space * 37 + "Molex Connected Enterprise Solutions Sp. z o.o. © all rights reserved",
                            font=("Malgun Gothic Semilight", 12), background='#9B9797', foreground='#1F1E1F', width=200)
    footerLabel.place(relx=0, rely=0.92)
    # ==== Buttons ====
    butt1 = ttk.Button(root, text="Search", command=findButtonHandle).place(x=40, y=200)
    butt2 = ttk.Button(root, text="Close", command=root.destroy).place(x=240, y=200)
    butt3 = ttk.Button(root, text="...", command=browse_button, width=4).place(x=500, y=90)

    # ==== Table configuration ====
    frame = Frame(root, width=500, height=0)
    frame.place(x=40, y=250)

    # Style configuration of the table
    style = ttk.Style(frame)
    style.theme_use("clam")
    style.configure("Treeview", background="#7F7979",
                    fieldbackground="#7F7979", foreground="white")

    list = ttk.Treeview(frame, height=8)
    list.pack()

    vsb = ttk.Scrollbar(root, orient="vertical", command=list.yview)
    vsb.place(x=802, y=250, height=189)

    list.configure(yscrollcommand=vsb.set)

    list['columns'] = (
        'MAC address', 'Time Stamp', 'Date', 'Model', 'Worker ID', 'Current Test', 'Voltage Test', 'Power Test',
        'Com Test')

    list.column("#0", width=0, stretch=NO)
    list.column("MAC address", anchor=CENTER, width=120)
    list.column("Time Stamp", anchor=CENTER, width=80)
    list.column("Date", anchor=CENTER, width=80)
    list.column("Model", anchor=CENTER, width=80)
    list.column("Worker ID", anchor=CENTER, width=80)
    list.column("Current Test", anchor=CENTER, width=80)
    list.column("Voltage Test", anchor=CENTER, width=80)
    list.column("Power Test", anchor=CENTER, width=80)
    list.column("Com Test", anchor=CENTER, width=80)

    list.heading("#0", text="", anchor=CENTER)
    list.heading("MAC address", text="MAC address", anchor=CENTER)
    list.heading("Time Stamp", text="Time Stamp", anchor=CENTER)
    list.heading("Date", text='Date', anchor=CENTER)
    list.heading("Model", text='Model', anchor=CENTER)
    list.heading("Worker ID", text="Worker ID", anchor=CENTER)
    list.heading("Current Test", text="Current Test", anchor=CENTER)
    list.heading("Voltage Test", text="Voltage Test", anchor=CENTER)
    list.heading("Power Test", text="Power Test", anchor=CENTER)
    list.heading("Com Test", text="Com Test", anchor=CENTER)

    root.mainloop()
