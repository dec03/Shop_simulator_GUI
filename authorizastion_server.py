#create a apple store
#one file to be a client
#one file to be a server
#one file to be a database (sql workbench)
#one file to be a shopkeeper client

#----server
#server need to be able to take requests from client and change the database accordingly
#eg, client adds iphone 11 to basket and confirms purchase,
#the server should update database to take out 1 iphone 11 stock
#and send the shopkeeper a recent purchase containing:
#order number,
#how much they made,
#what they bought,
#the stock remaining

#----client
#client should be able to see the available options
#client should be able to add to basket
#client should be able to take out of basket
#client should be able to clear basket
#client should be able to pay and order and it should display a pop up message saying the final cost
#it should ask the user are veryify whether they want to go through with the order,
#if yes, then process transactions and output 'thank you for your purchase',
#then update database through server
#if no, go back to previous menu/function

#----shopkeeper
#shopkeeper should be able to see automated updates of recent purchases by customers
#they should be able to see:
#order number,
#how much they made,
#what they bought,
#the stock remaining

#use execfile() for this

import mysql.connector
import socket
import _thread
import threading
import socket
import _tkinter
import tkinter.font as font
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import os

#------------Functions------------
def timer():
    global timeout_timer
    global tries
    global length_of_time

    timeout = threading.Timer(0.2, timer)
    timeout.start()

    if timeout_timer == length_of_time:
        #when time limit has been met, it resets the wigits so its editable
        pass_entry = Entry(mainFrame,
        textvariable=two,
        bg='white',
        font=('Times new roman', 12),
        width=16,
        show='*',
        state=NORMAL).place(x=120,y=200)

        user_entry = Entry(mainFrame,
        textvariable=one,
        bg='white',
        font=('Times new roman', 12),
        width=16,
        state=NORMAL).place(x=120,y=120)

        #cancels thread
        timeout.cancel()
        timeout_timer = 0
        tries = 0
    else:
        #timer increments
        timeout_timer += 1
        return


def check_info():
    global tries
    global pass_entry
    global user_entry
    global length_of_time

    user_ = one.get()
    pass_ = two.get()
    #print(user_,pass_)
    user_found = False
    pass_found = False

    for i in server_accounts:
        #if user is found
        if i[1] == user_:
            #sets user found to true
            user_found == True
            #if password is found next to it
            if i[2] == pass_:
                pass_entry = Entry(mainFrame,
                textvariable=two,
                bg='light green',
                font=('Times new roman', 12),
                width=16,
                show='*',
                state=DISABLED).place(x=120,y=200)

                user_entry = Entry(mainFrame,
                textvariable=one,
                bg='light green',
                font=('Times new roman', 12),
                width=16,
                state=DISABLED).place(x=120,y=120)
                #if the username and password matches and is in the database
                root.destroy()
                #it will load the server GUI and execute that file
                exec(open("./server.py").read())
            else:
                #sets the password found to false meaning the username is correct
                #but the password isnt
                pass_found = False
                break
        else:
            #continues the for loop if the username at that index is not matched
            continue

    if user_found == False:
        #user_entry.configure({"background": "red"})
        #pass_entry.configure({"background": "red"})
        messagebox.showwarning(title='Invalid Input', message='Username is Incorrect')
        tries += 1
        if tries == 5:
            messagebox.showerror(title='Timeout', message='You have made too many attempts')
            pass_entry = Entry(mainFrame,
            textvariable=two,
            bg='red',
            font=('Times new roman', 12),
            width=16,
            show='*',
            state=DISABLED).place(x=120,y=200)

            user_entry = Entry(mainFrame,
            textvariable=one,
            bg='red',
            font=('Times new roman', 12),
            width=16,
            state=DISABLED).place(x=120,y=120)
            length_of_time += 30
            timer()
        else:
            return

    elif user_found == True and pass_found != True:
        #user_entry.configure({"background": "red"})
        #pass_entry.configure({"background": "red"})
        messagebox.showwarning(title='Invalid Input', message='Password is Incorrect')
        tries += 1
        if tries == 5:
            messagebox.showerror(title='Timeout', message='You have made too many attempts')
            pass_entry = Entry(mainFrame,
            textvariable=two,
            bg='red',
            font=('Times new roman', 12),
            width=16,
            show='*',
            state=DISABLED).place(x=120,y=200)

            user_entry = Entry(mainFrame,
            textvariable=one,
            bg='red',
            font=('Times new roman', 12),
            width=16,
            state=DISABLED).place(x=120,y=120)
            length_of_time += 30
            timer()
        else:
            return



mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=''
)
#this is used to naviagte and interact with the database
mycursor = mydb.cursor()
server_accounts = []
#this gets all records from the table
mycursor.execute('SELECT * FROM authentication_accounts')
#this stores the result pulled into server accounts_fetch
server_accounts_fetch = mycursor.fetchall()
#this appends each record to server_accounts
for x in server_accounts_fetch:
    server_accounts.append(x)


tries = 0
timeout_timer = 0
length_of_time = 10


#main window
root = Tk()
#sets window background colour
root.configure(bg='black')
#sets window size but is still resizable
root.geometry('300x400')
#makes window unresizable
root.resizable(False, False)
#makes title of window apple store
root.title('Server Authentication')



#--------------frames--------------
mainFrame = Frame(root,
width=500,
height=600,
background='#ddcbaa')
mainFrame.pack()

title = Frame(mainFrame,
width=500,
height=100,
bg='white',
relief=RAISED)
title.place(x=0,y=0)

#-------------wigits---------------
title_s = Label(title,
bg='white',
text='Sign In To Access Server',
font=('Times new roman', 14),
relief=RAISED,
width=30,
height=3).pack()

#username entry
username = Label(mainFrame,
bg='#ddcbaa',
text='Username',
font=('Times new roman', 14)).place(x=20,y=120)

one = StringVar()
user_entry = Entry(mainFrame,
textvariable=one,
bg='white',
font=('Times new roman', 12),
width=16,
state=NORMAL).place(x=120,y=120)

#password entry
password = Label(mainFrame,
bg='#ddcbaa',
text='Password',
font=('Times new roman', 14)).place(x=20,y=200)

two = StringVar()
pass_entry = Entry(mainFrame,
textvariable=two,
bg='white',
font=('Times new roman', 12),
width=16,
show='*',
state=NORMAL).place(x=120,y=200)

#login button
login = Button(mainFrame,
bg='white',
font=('Times new roman', 14),
width=18,
height=3,
relief=RAISED,
text='Login',
activebackground='lightblue',
command=check_info).place(x=55,y=300)

root.mainloop()
