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

import mysql.connector
import socket
import _thread
import threading
import socket
import _tkinter
import tkinter.font as font
import mysql.connector
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter.scrolledtext import ScrolledText

#-------------AccessToDatabase--------------------
mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=''
)

#this is used to naviagte and interact with the database
mycursor = mydb.cursor()

#query
mycursor.execute("SELECT * FROM stock")
#stores all the records of data in list variable stock_in (list)
stock_in = mycursor.fetchall()
stock_to_use = []
stock_for_pk = []
#outputs results
for x in stock_in:
    stock_to_use.append(x[1:])
    stock_for_pk.append(x)

stock = [list(item) for item in stock_to_use]
stock_pk = [list(item) for item in stock_for_pk]

#---------------serverconnections-------------------
clients = []
client_name = []
num_of_entries = 0
#-----------------------------------------------------
# get the hostname
host = socket.gethostname()
port = 12345  # initiate port no above 1024
server_socket = socket.socket()  # get instance
server_socket.bind((host, port))  # bind host address and port together
# configure how many client the server can listen simultaneously
server_socket.listen()
while True:
    #----------------functions for connection------------
    def on_new_client(client_ip,client_address):
        client_pos = len(clients)
        while True:
            basket = []
            final_basket = client_ip.recv(1024).decode()
            #if server recieves quit from a clinet it will disconnect them from the server
            if final_basket == 'quit_':
                break
            #turns list string back to list
            final_basket = eval(final_basket)
            if final_basket[-1] != 'Purchase':
                #to retrun if iphone is in stock
                if 'Iphone' in final_basket[0]:
                    #changes the string price to float to compare
                    change_string_int = final_basket[4]
                    #takes out £ and turns to float
                    change_string_int = float(change_string_int[1:])
                    final_basket[4] = change_string_int
                    #checks if item sent by client is in stock in the database
                    for i in range(0,len(stock)):
                            if final_basket[0] == stock[i][0] and final_basket[1] == stock[i][1] and final_basket[2] == stock[i][2] and final_basket[3] == stock[i][3] and final_basket[4] == stock[i][4]:
                                if stock[i][5] != 0:
                                    msg = 'In Stock'
                                    clients[client_pos].send(msg.encode())
                                    break
                                elif stock[i][5] == 0:
                                    msg = 'not in stock'
                                    clients[client_pos].send(msg.encode())
                            else:
                                continue

                #to return if airpods in stock
                elif 'Air Pods' in final_basket[0]:
                    if final_basket[1] != 'Max':
                        #changes the string price to float to compare
                        change_string_int = final_basket[2]
                        #takes out £ and turns to float
                        change_string_int = float(change_string_int[1:])
                        final_basket[2] = change_string_int
                        #checks if item sent by client is in stock in the database
                        for i in range(0,len(stock)):
                            if final_basket[0] == stock[i][0] and final_basket[1] == stock[i][1] and final_basket[2] == stock[i][4]:
                                if stock[i][5] != 0:
                                    msg = 'In Stock'
                                    clients[client_pos].send(msg.encode())
                                    break
                                elif stock[i][5] == 0:
                                    msg = 'not in stock'
                                    clients[client_pos].send(msg.encode())
                            else:
                                continue
                    elif final_basket[1] == 'Max':
                        #changes the string price to float to compare
                        change_string_int = final_basket[3]
                        #takes out £ and turns to float
                        change_string_int = float(change_string_int[1:])
                        final_basket[3] = change_string_int
                        #checks if item sent by client is in stock in the database
                        for i in range(0,len(stock)):
                            if final_basket[1] == stock[i][1] and final_basket[2] == stock[i][3] and final_basket[3] == stock[i][4]:
                                if stock[i][5] != 0:
                                    msg = 'In Stock'
                                    clients[client_pos].send(msg.encode())
                                    break
                                elif stock[i][5] == 0:
                                    msg = 'not in stock'
                                    clients[client_pos].send(msg.encode())
                            else:
                                continue

            if final_basket[-1] == 'Purchase':
                #gets total price
                price = 0
                for i in final_basket[:-1]:
                    temp = i[-1]
                    temp = float(temp[1:])
                    price += temp
                for i in final_basket:
                    #updates database
                    if 'Iphone' in i[0]:
                        name = str(i[0])
                        model = str(i[1])
                        storage = str(i[2])
                        colour = str(i[3])
                        for x in stock_pk:
                            if name in x and model in x and storage in x and colour in x:
                                #if item in items basket matches the data in the database table
                                #it will get the product number and update the table
                                product_num = str(x[0])
                                query = "UPDATE stock SET stock_num = stock_num - 1 WHERE product_num = %s"
                                mycursor.execute(query, (product_num,))
                                mydb.commit()
                                #this will output what records have been updated to the
                                #server which the shopkeeper will see
                                mycursor.execute("SELECT * FROM stock WHERE product_num = %s", (product_num,))
                                result = mycursor.fetchall()
                                updated_stock_from_clients['state'] = NORMAL
                                updated_stock_from_clients.insert(INSERT, f'Stock Update for: {result[-1][:-2]} | {result[-1][-1]}\n')
                                updated_stock_from_clients['state'] = DISABLED
                            else:
                                continue

                    elif 'Air Pod' in i[0]:
                        if i[1] == 'Max':
                            name = str(i[0])
                            model = str(i[1])
                            colour = str(i[2])
                            for x in stock_pk:
                                if name[0:-4] in x and model in x and colour in x:
                                    #if item in items basket matches the data in the database table
                                    #it will get the product number and update the table
                                    product_num = str(x[0])
                                    query = "UPDATE stock SET stock_num = stock_num - 1 WHERE product_num = %s"
                                    mycursor.execute(query, (product_num,))
                                    mydb.commit()
                                    #this will output what records have been updated to the
                                    #server which the shopkeeper will see
                                    mycursor.execute("SELECT * FROM stock WHERE product_num = %s", (product_num,))
                                    result = mycursor.fetchall()
                                    updated_stock_from_clients['state'] = NORMAL
                                    updated_stock_from_clients.insert(INSERT, f'Stock Update for: {result[-1][:-2]} | {result[-1][-1]}\n')
                                    updated_stock_from_clients['state'] = DISABLED
                                else:
                                    continue
                        elif i[1] != 'Max':
                            name = str(i[0])
                            model = str(i[1])
                            for x in stock_pk:
                                if name in x and model in x:
                                    #if item in items basket matches the data in the database table
                                    #it will get the product number and update the table
                                    product_num = str(x[0])
                                    query = "UPDATE stock SET stock_num = stock_num - 1 WHERE product_num = %s"
                                    mycursor.execute(query, (product_num,))
                                    mydb.commit()
                                    #this will output what records have been updated to the
                                    #server which the shopkeeper will see
                                    mycursor.execute("SELECT * FROM stock WHERE product_num = %s", (product_num,))
                                    result = mycursor.fetchall()
                                    updated_stock_from_clients['state'] = NORMAL
                                    updated_stock_from_clients.insert(INSERT, f'Stock Update for: {result[-1][:-2]} | {result[-1][-1]}\n')
                                    updated_stock_from_clients['state'] = DISABLED
                                else:
                                    continue

                #this will send the final price of the purchase to the user
                conn.send(str(price).encode())
                price = str(price) + '0'
                #this updates the purchases made from clients box so the shopkeeper can see the revenue they have made
                purchases_from_clients['state'] = NORMAL
                purchases_from_clients.insert(INSERT, f'{client_address[1]}/{client_name[client_pos]} - Order Came to: £{price}\n')
                purchases_from_clients['state'] = DISABLED


        #CHANGES STATE to normal so the box can written to
        server_connection_from_client['state'] = NORMAL
        #inserts who connected to server
        server_connection_from_client.insert(INSERT,f'{client_address}/{client_name[client_pos]}: disconnected\n')
        #sets the state back to disable so the data cant be changed
        server_connection_from_client['state'] = DISABLED
        clients.remove(conn)
        client_name.delete(client_pos)
        client_ip.close()
    #-------------------connections-------------------------------
    conn, client_address = server_socket.accept()  # accept new connection
    #starts new thread to handle client
    _thread.start_new_thread(on_new_client,(conn,client_address))

    msg = 'Hello, What is your name?'
    conn.send(msg.encode())

    #recieves and decodes message
    c_name = conn.recv(1024).decode()
    #print(f'Clients name is: {c_name}')

    #adds name and client ip to list
    client_name.append(c_name)

    #-----------------GUI--------------------
    #main window
    root = Tk()
    #sets window background colour
    root.configure(bg='black')
    #sets window size but is still resizable
    root.geometry('500x600')
    #makes window unresizable
    root.resizable(False, False)
    #makes title of window apple store
    root.title('Sever_Logs')

    #----------------frames-----------------------
    mainFrame = Frame(root,
    width=500,
    height=600,
    background='#1d3868')
    mainFrame.pack()

    content = Frame(mainFrame,
    width=450,
    height=550,
    background='#ddcbaa')
    content.place(x=24,y=20)

    #--------------------wigits-------------------
    #TEXTBOX TITLE for server connections
    server_connection_from_client_title = Label(content,
    text = 'Connections To Server',
    font=('times new roman', 12),
    relief=RAISED)
    server_connection_from_client_title.place(x=44,y=10)
    #TEXTBOX for outputting new connections
    server_connection_from_client = ScrolledText(content,
    width = 32,
    height = 10,
    font=('times new roman', 8),
    relief = SUNKEN,
    state=DISABLED)
    server_connection_from_client.place(x=8,y=40)




    #TEXTBOX TITLE for purchases made by the clients
    purchases_from_clients_title = Label(content,
    text = 'Purchases By Clients',
    font=('times new roman', 12),
    relief=RAISED)
    purchases_from_clients_title.place(x=271,y=10)
    #textbox For outtputting purchases made by clients
    purchases_from_clients = ScrolledText(content,
    width = 30,
    height = 10,
    font=('times new roman', 8),
    relief = SUNKEN,
    state=DISABLED)
    purchases_from_clients.place(x=233,y=40)



    #TEXTBOX TITLE for Stock updates
    stock_update_title = Label(content,
    text = 'Stock Updates',
    font=('times new roman', 12),
    relief=RAISED)
    stock_update_title.place(x=180,y=220)
    #textbox For outtputting the updated records
    updated_stock_from_clients = ScrolledText(content,
    width = 68,
    height = 20,
    font=('times new roman', 8),
    relief = SUNKEN,
    state=DISABLED)
    updated_stock_from_clients.place(x=9,y=250)


    #puts client ip into clients list
    clients.append(conn)
    #changes num of entries to +1
    num_of_entries += 1
    #CHANGES STATE to normal so the box can written to
    server_connection_from_client['state'] = NORMAL
    #inserts who connected to server
    server_connection_from_client.insert(INSERT,f'{client_address}/{c_name}: connected\n')
    #sets the state back to disable so the data cant be changed
    server_connection_from_client['state'] = DISABLED

    root.mainloop()
