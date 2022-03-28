#create a apple store
#one file to be a client
#one file to be a server
#one file to be a database (sql workbench)
#one file to be a shopkeeper client

#----server for shopkeeper
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



#everytime the user adds to basket or removes, get attributes of what they added and add it to a list as one item
import socket
import _thread
import threading
import _tkinter
import tkinter.font as font
import pickle
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from time import time
from PIL import ImageTk, Image
from tkinter.scrolledtext import ScrolledText


#----------------------connections-----------------
host = socket.gethostname()
port = 12345

c_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
con = c_s.connect((host, port))

sleep_count = 0

#-------------gui-------------------------
while True:
    #main window
    root = Tk()
    #sets window background colour
    root.configure(bg='black')
    #sets window size but is still resizable
    root.geometry('500x600')
    #makes window unresizable
    root.resizable(False, False)
    #makes title of window apple store
    root.title('Apple Store')

    #-------------functions-----------------------
    def continue_y():
        #kills the continue wigit to continue shopping
        for widget in root.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()
        return

    def continue_n():
        #this send quit to the server to signal a disconnect
        msg = 'quit_'
        c_s.send(msg.encode())
        for widget in root.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()

        iphone13_thread.cancel()
        iphone12_thread.cancel()
        iphone11_thread.cancel()
        iphoneSE_thread.cancel()
        airpod_thread.cancel()
        airpodmax_thread.cancel()

        root.quit()
        quit()
        return

    #this function will reset everything and also clear the basket
    def clear_everything():
        basket_num.set('0')
        contents_of_basket.clear()
        quantity_13_value.set('0')
        quantity_12_value.set('0')
        quantity_SE_value.set('0')
        quantity_11_value.set('0')
        quantity_airpod_value.set('0')
        quantity_airpodmax_value.set('0')
        for widget in root.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()
        #reopens basket window after its destroyed
        basket_window()

    #this processes the items and makes a transaction for the server
    def purchase_final():
        #appends purchase at the end of the list so the server
        #recognises its a purchase being made
        contents_of_basket.append('Purchase')
        #this send the contents in the basket to the server
        c_s.send(str(contents_of_basket).encode())
        #this recieves the price sent by the server after the the server
        #has updated the database
        price_total = '£' + c_s.recv(1024).decode()
        price_total = price_total + '0'
        #this gets the price after VAT
        price_vat = float(price_total[1:]) + (((float(price_total[1:]) / 100) * 5))
        price_vat = '£' + str(price_vat) + '0'
        #this outputs the receipt
        messagebox.showinfo('Purchase Receipt', f'Hello {name_of_user}\n\nThe Items you have purchased:\n{contents_of_basket[:-1]}\n\nTotal: {price_total}\n\nFinal Total (5% VAT): {price_vat}')

        #this resets everything and clears the basket
        basket_num.set('0')
        contents_of_basket.clear()
        quantity_13_value.set('0')
        quantity_12_value.set('0')
        quantity_SE_value.set('0')
        quantity_11_value.set('0')
        quantity_airpod_value.set('0')
        quantity_airpodmax_value.set('0')
        for widget in root.winfo_children():
            if isinstance(widget, Toplevel):
                widget.destroy()

        #creates a new window
        continue_window_app = Toplevel(root)
        #changes the title of the new window to user
        continue_window_app.title('Client')
        #changes the size of the window
        continue_window_app.geometry('400x150')
        #makes window unresizable
        continue_window_app.resizable(False, False)

        #create a label outputting the message
        vis=Label(continue_window_app,
        text=f'Would you like to continue shopping {name_of_user}',
        font=(8),
        relief=RAISED).place(x=40,y=0)

        #these two buttons will allow the user to decide whether they
        #would like to continue shopping or not
        yes=Button(continue_window_app,
        font=('times new roman', 10),
        text='Yes',
        command=continue_y)
        yes.place(x=80,y=50)
        no=Button(continue_window_app,
        font=('times new roman', 10),
        text='No',
        command=continue_n)
        no.place(x=270,y=50)



    #this is a function that creates a basket window for the user to view the products
    #they want to purchase
    def basket_window():
        #creates a new window
        basket_window_app = Toplevel(root)
        #changes the title of the new window to Basket
        basket_window_app.title('Basket')
        #changes the size of the window
        basket_window_app.geometry('450x600')
        #makes window unresizable
        basket_window_app.resizable(False,False)
        #entry box that contains the items in the basket
        basket_contents = ScrolledText(basket_window_app,
        bg = 'white',
        width = 50)
        basket_contents.place(x=20,y=20, height=520)
        #this stores the items that the user wants to the basket
        for i in range(0,len(contents_of_basket)):
            Button(basket_contents,
            text=contents_of_basket[i],
            width=80,
            font=('times new roman', 7),
            justify=LEFT).grid(column=0,row=i)

        #this is a button that processes the clients basket
        transaction = Button(basket_window_app,
        text='Purchase items',
        width=20,
        font=('times new roman', 10),
        command=purchase_final).place(x=22,y=550, height=40)

        #this button clears all items from the basket
        clear_basket = Button(basket_window_app,
        text='Clear Basket',
        width=20,
        font=('times new roman', 10),
        command=clear_everything).place(x=282,y=550, height=40)

    #counter that increments the sleep count variable
    #then destroys the window at 5 seconds
    def sleep_counter():
        global sleep_count
        #this starts a timer thread that will go
        #through this function every second
        counter = threading.Timer(1, sleep_counter)
        counter.start()
        if sleep_count == 5:
            #stops thread
            counter.cancel()
            #destroy toplevel after 5 seconds
            name_window_app.destroy()
            sleep_count=0
            return
        else:
            sleep_count += 1
            return

    #this function sends the name of the client to the server
    def send_name(name_user):
        global name_of_user
        #gets users input and send to server
        name_user = str(entry_box.get())
        name_of_user = str(entry_box.get())
        #if the name of the user is blank, it will exit the function
        if name_user == '':
            return
        #if its not blank it will send the users input to the server
        name.delete(0,END)
        c_s.send(name_user.encode())
        #create a label outputting the message
        vis=Label(name_window_app,
        text=f'Hello {name_user}',
        font=(8),
        relief=RAISED).place(x=80,y=100)
        sleep_counter()
        return



    #------functions to update price-------------
    #all of these functions use thread timers to update all of the prices for each product
    def get_price_iphone_13():
        iphone13_thread = threading.Timer(0.1,get_price_iphone_13)
        iphone13_thread.start()
        model_temp13 = str(iphone13_model.get())
        storage_temp13 = str(iphone13_storage.get())
        if model_temp13 == 'Pro Max':
            if storage_temp13 == '128GB':
                price_13.set("£1049.00")
            elif storage_temp13 == '256GB':
                price_13.set("£1149.00")
            elif storage_temp13 == '512GB':
                price_13.set("£1349.00")
            elif storage_temp13 == '1TB':
                price_13.set("£1549.00")

        elif model_temp13 == 'Pro':
            if storage_temp13 == '128GB':
                price_13.set("£949.00")
            elif storage_temp13 == '256GB':
                price_13.set("£1049.00")
            elif storage_temp13 == '512GB':
                price_13.set("£1249.00")
            elif storage_temp13 == '1TB':
                price_13.set("£1449.00")
        return

    def get_price_iphone_12():
        iphone12_thread = threading.Timer(0.1,get_price_iphone_12)
        iphone12_thread.start()
        model_temp12 = str(iphone12_model.get())
        storage_temp12 = str(iphone12_storage.get())
        if model_temp12 == 'Mini':
            if storage_temp12 == '64GB':
                price_12.set("£579.00")
            elif storage_temp12 == '128GB':
                price_12.set("£629.00")
            elif storage_temp12 == '256GB':
                price_12.set("£729.00")

        elif model_temp12 == 'Normal':
            if storage_temp12 == '64GB':
                price_12.set("£679.00")
            elif storage_temp12 == '128GB':
                price_12.set("£729.00")
            elif storage_temp12 == '256GB':
                price_12.set("£829.00")
        return

    def get_price_iphone_SE():
        iphoneSE_thread = threading.Timer(0.1,get_price_iphone_SE)
        iphoneSE_thread.start()
        model_tempSE = str(iphoneSE_model.get())
        storage_tempSE = str(iphoneSE_storage.get())
        if model_tempSE == 'Normal':
            if storage_tempSE == '64GB':
                price_SE.set("£389.00")
            elif storage_tempSE == '128GB':
                price_SE.set("£429.00")
        return

    def get_price_iphone_11():
        iphone11_thread = threading.Timer(0.1,get_price_iphone_11)
        iphone11_thread.start()
        model_temp11 = str(iphone11_model.get())
        storage_temp11 = str(iphone11_storage.get())
        if model_temp11 == 'Normal':
            if storage_temp11 == '64GB':
                price_11.set("£489.00")
            elif storage_temp11 == '128GB':
                price_11.set("£539.00")
        return

    def get_price_airpods():
        airpod_thread = threading.Timer(0.1,get_price_airpods)
        airpod_thread.start()
        model_tempairpod = str(airpod_model.get())
        if model_tempairpod == '2nd Generation':
            price_airpod.set("£119.00")
        elif model_tempairpod == '3rd Generation':
            price_airpod.set("£169.00")
        elif model_tempairpod == 'Pro':
            price_airpod.set("£239.00")
        return

    def get_price_airpods_max():
        airpodmax_thread = threading.Timer(0.1,get_price_airpods_max)
        airpodmax_thread.start()
        model_tempairpodmax = str(airpodmax_model.get())
        if model_tempairpodmax == 'Max':
            price_airpodmax.set("£549.00")
        return

    #-----------functions to change quantity-------
    #all of these functions are used to check if the items are in stock
    #by getting the attributes of the products and sending it to the server
    #to check if the item in the database is in stock or not
    #if its in stock it will allow the user to add the item to basket
    #if its not in stock it will show a infobox saying item is not in stock

    #the add items will add the items to the basket
    def quantity_for_13_add():
        temp_list = []
        temp_list.append('Iphone 13')
        temp_list.append(str(iphone13_model.get()))
        temp_list.append(str(iphone13_storage.get()))
        temp_list.append(str(iphone13_colour.get()))
        temp_list.append(str(price_13.get()))
        c_s.send(str(temp_list).encode())
        recieve_req = c_s.recv(1024).decode()
        if recieve_req == 'In Stock':
            basket_update = basket_num.get() + 1
            update = quantity_13_value.get()
            update += 1
            contents_of_basket.append(temp_list)
            basket_num.set(basket_update)
            quantity_13_value.set(update)
        else:
            messagebox.showinfo('Item Out Of Stock', 'Sorry, but this item is out of stock')

    #the sub functions will take out items from the basket
    def quantity_for_13_sub():
        update = quantity_13_value.get()
        if update != 0:
            temp_list = []
            temp_list.append('Iphone 13')
            temp_list.append(str(iphone13_model.get()))
            temp_list.append(str(iphone13_storage.get()))
            temp_list.append(str(iphone13_colour.get()))
            temp_list.append(str(price_13.get()))
            if temp_list in contents_of_basket:
                basket_update = basket_num.get() - 1
                basket_num.set(basket_update)
                update -= 1
                quantity_13_value.set(update)

                contents_of_basket.remove(temp_list)
            else:
                return
        return

    def quantity_for_12_add():
        temp_list = []
        temp_list.append('Iphone 12')
        temp_list.append(str(iphone12_model.get()))
        temp_list.append(str(iphone12_storage.get()))
        temp_list.append(str(iphone12_colour.get()))
        temp_list.append(str(price_12.get()))
        c_s.send(str(temp_list).encode())
        recieve_req = c_s.recv(1024).decode()
        if recieve_req == 'In Stock':
            basket_update = basket_num.get() + 1
            update = quantity_12_value.get()
            update += 1
            contents_of_basket.append(temp_list)
            basket_num.set(basket_update)
            quantity_12_value.set(update)
        else:
            messagebox.showinfo('Item Out Of Stock', 'Sorry, but this item is out of stock')


    def quantity_for_12_sub():
        update = quantity_12_value.get()
        if update != 0:
            basket_update = basket_num.get() - 1
            basket_num.set(basket_update)
            update -= 1
            quantity_12_value.set(update)
        return

    def quantity_for_11_add():
        temp_list = []
        temp_list.append('Iphone 11')
        temp_list.append(str(iphone11_model.get()))
        temp_list.append(str(iphone11_storage.get()))
        temp_list.append(str(iphone11_colour.get()))
        temp_list.append(str(price_11.get()))
        c_s.send(str(temp_list).encode())
        recieve_req = c_s.recv(1024).decode()
        if recieve_req == 'In Stock':
            basket_update = basket_num.get() + 1
            update = quantity_11_value.get()
            update += 1
            contents_of_basket.append(temp_list)
            basket_num.set(basket_update)
            quantity_11_value.set(update)
        else:
            messagebox.showinfo('Item Out Of Stock', 'Sorry, but this item is out of stock')

    def quantity_for_11_sub():
        update = quantity_11_value.get()
        if update != 0:
            basket_update = basket_num.get() - 1
            basket_num.set(basket_update)
            update -= 1
            quantity_11_value.set(update)
        return

    def quantity_for_SE_add():
        temp_list = []
        temp_list.append('Iphone SE')
        temp_list.append(str(iphoneSE_model.get()))
        temp_list.append(str(iphoneSE_storage.get()))
        temp_list.append(str(iphoneSE_colour.get()))
        temp_list.append(str(price_SE.get()))
        c_s.send(str(temp_list).encode())
        recieve_req = c_s.recv(1024).decode()
        if recieve_req == 'In Stock':
            basket_update = basket_num.get() + 1
            update = quantity_SE_value.get()
            update += 1
            contents_of_basket.append(temp_list)
            basket_num.set(basket_update)
            quantity_SE_value.set(update)
        else:
            messagebox.showinfo('Item Out Of Stock', 'Sorry, but this item is out of stock')


    def quantity_for_SE_sub():
        update = quantity_SE_value.get()
        if update != 0:
            basket_update = basket_num.get() - 1
            basket_num.set(basket_update)
            update -= 1
            quantity_SE_value.set(update)
        return

    def quantity_for_airpod_add():
        temp_list = []
        temp_list.append('Air Pods')
        temp_list.append(str(airpod_model.get()))
        temp_list.append(str(price_airpod.get()))
        c_s.send(str(temp_list).encode())
        recieve_req = c_s.recv(1024).decode()
        if recieve_req == 'In Stock':
            basket_update = basket_num.get() + 1
            update = quantity_airpod_value.get()
            update += 1
            contents_of_basket.append(temp_list)
            basket_num.set(basket_update)
            quantity_airpod_value.set(update)
        else:
            messagebox.showinfo('Item Out Of Stock', 'Sorry, but this item is out of stock')


    def quantity_for_airpod_sub():
        update = quantity_airpod_value.get()
        if update != 0:
            basket_update = basket_num.get() - 1
            basket_num.set(basket_update)
            update -= 1
            quantity_airpod_value.set(update)
        return

    def quantity_for_airpodmax_add():
        temp_list = []
        temp_list.append('Air Pods Max')
        temp_list.append(str(airpodmax_model.get()))
        temp_list.append(str(airpodmax_colour.get()))
        temp_list.append(str(price_airpodmax.get()))
        c_s.send(str(temp_list).encode())
        recieve_req = c_s.recv(1024).decode()
        if recieve_req == 'In Stock':
            basket_update = basket_num.get() + 1
            update = quantity_airpodmax_value.get()
            update += 1
            contents_of_basket.append(temp_list)
            basket_num.set(basket_update)
            quantity_airpodmax_value.set(update)
        else:
            messagebox.showinfo('Item Out Of Stock', 'Sorry, but this item is out of stock')


    def quantity_for_airpodmax_sub():
        update = quantity_airpodmax_value.get()
        if update != 0:
            basket_update = basket_num.get() - 1
            basket_num.set(basket_update)
            update -= 1
            quantity_airpodmax_value.set(update)
        return
    #------------global-variables------------------
    #stores the number of items in the basket
    basket_num = IntVar()
    basket_num.set('0')
    contents_of_basket = []
    #stores the name of the user
    name_of_user = ''

    #----------------frames------------------------

    #frames
    mainFrame = Frame(root,
    width=500,
    height=600,
    background='#1d3868')
    mainFrame.pack()

    #frame for title
    top_title = Frame(mainFrame,
    width=500,
    height=50,
    bg='white')
    top_title.place(x=0,y=0)

    #frame for main content
    content = Frame(mainFrame,
    width=400,
    height=500,
    background='black')
    content.place(x=40,y=75)

    #----------------images--------------------
    #opens and assigns image to variable
    img = Image.open("basket.jpg")
    resize_basket = img.resize((50,35))
    basket_img = ImageTk.PhotoImage(resize_basket)

    #----------------wigits---------------------
    #a label containing the title
    title = Label(top_title,
    width=42,
    height=3,
    font=('Times New Roman', 16),
    text='Welcome To Apple Store',
    relief=RAISED,
    bg='white',
    fg='black')
    title.pack()

    #a canvas which stores all the main contents of the app
    canvas = Canvas(content,
    width=400,
    height=500,
    bg='white')
    scroll_bar = Scrollbar(content,
    orient='vertical',
    relief=SUNKEN,
    command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_bar.set)
    canvas.pack(side='left')
    scroll_bar.pack(side='right',fill='y')

    #image for basket which is also a button which when
    #pressed will open a basket window to view basket
    img_for_basket = Button(canvas,
    image=basket_img,
    relief=GROOVE,
    command=basket_window).place(x=345,y=2)

    #this shows the user the amount of items in the basket
    count_basket = Label(canvas,
    textvariable=basket_num,
    font=('Times New Roman', 16),
    bg='white').place(x=315,y=8)



    #--------------gets request to send name to server-------
    message = c_s.recv(1024).decode()  # receive response

    if message == 'Hello, What is your name?':
        #creates a new window
        name_window_app = Toplevel(root)
        #changes the title of the new window to user
        name_window_app.title('Client')
        #changes the size of the window
        name_window_app.geometry('250x150')
        #makes window unresizable
        name_window_app.resizable(False, False)

        #create a label outputting the message
        vis=Label(name_window_app,
        text=message,
        font=(8),
        relief=RAISED).place(x=35,y=0)

        #create entry box to allow user to input name
        entry_box = StringVar()
        name=Entry(name_window_app,
        font=('times new roman', 8),
        textvariable=entry_box)
        name.bind("<Return>", send_name)
        name.place(x=65,y=50)

    #-----------Options for user to purchase---------
    #this lets the user know what the product is
    iphone13 = Label(canvas,
    text='Iphone 13',
    width=10,
    height=2,
    relief=RAISED).place(x=5,y=50)
    #this gets the model that the user chooses
    iphone13_models_choice = ('Pro Max', 'Pro')
    iphone13_model = Combobox(canvas,
    state='readonly',
    width=8,
    height=1,
    values=iphone13_models_choice)
    iphone13_model.current(0)
    iphone13_model.place(x=85, y=60)
    #this gets the storage that the user chooses
    iphone13_storage_choice = ('1TB', '512GB', '256GB', '128GB')
    iphone13_storage = Combobox(canvas,
    state='readonly',
    width=6,
    height=1,
    values=iphone13_storage_choice)
    iphone13_storage.current(0)
    iphone13_storage.place(x=165, y=60)
    #this gets the colour that the user chooses
    iphone13_colour_choice = ('Sierra Blue', 'Silver', 'Graphite', 'Gold')
    iphone13_colour = Combobox(canvas,
    state='readonly',
    width=10,
    height=1,
    values=iphone13_colour_choice)
    iphone13_colour.current(0)
    iphone13_colour.place(x=235, y=60)
    #this gets the price
    price_13 = StringVar()
    iphone13_price = Label(canvas,
    textvariable = price_13,
    width=8,
    height=1,
    relief=RAISED).place(x=325,y=60)
    #this takes out items from the basket by running the sub function
    subtract_13 = Button(canvas,
    text = '-',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_13_sub).place(x=325, y=85)
    #this stores the amount of items selected from the product
    quantity_13_value = IntVar()
    quantity_13 = Entry(canvas,
    textvariable = quantity_13_value,
    width = 4,
    justify=CENTER,
    relief = SUNKEN).place(x=343, y=88)
    quantity_13_value.set(0)
    #this adds items into the basket that the client chooses
    add_13 = Button(canvas,
    text = '+',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_13_add).place(x=371, y=85)


    #-------------------------------------
    iphone12 = Label(canvas,
    text='Iphone 12',
    width=10,
    height=2,
    relief=RAISED).place(x=5,y=125)

    iphone12_models_choice = ('Normal', 'Mini')
    iphone12_model = Combobox(canvas,
    state='readonly',
    width=8,
    height=1,
    values=iphone12_models_choice)
    iphone12_model.current(0)
    iphone12_model.place(x=85, y=135)

    iphone12_storage_choice = ('256GB', '128GB', '64GB')
    iphone12_storage = Combobox(canvas,
    state='readonly',
    width=6,
    height=1,
    values=iphone12_storage_choice)
    iphone12_storage.current(0)
    iphone12_storage.place(x=165, y=135)

    iphone12_colour_choice = ('Purple', 'Blue', 'Green', 'White', 'Black', 'Red')
    iphone12_colour = Combobox(canvas,
    state='readonly',
    width=10,
    height=1,
    values=iphone12_colour_choice)
    iphone12_colour.current(0)
    iphone12_colour.place(x=235, y=135)

    price_12 = StringVar()
    iphone12_price = Label(canvas,
    textvariable =price_12,
    width=8,
    height=1,
    relief=RAISED).place(x=325,y=135)

    subtract_12 = Button(canvas,
    text = '-',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_12_sub).place(x=325, y=160)

    quantity_12_value = IntVar()
    quantity_12 = Entry(canvas,
    text = quantity_12_value,
    width = 4,
    justify=CENTER,
    relief = SUNKEN).place(x=343, y=163)
    quantity_12_value.set('0')

    add_12 = Button(canvas,
    text = '+',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_12_add).place(x=371, y=160)

    #-------------------------------------
    iphoneSE = Label(canvas,
    text='Iphone SE',
    width=10,
    height=2,
    relief=RAISED).place(x=5,y=200)

    iphoneSE_models_choice = ('Normal')
    iphoneSE_model = Combobox(canvas,
    state='readonly',
    width=8,
    height=1,
    values=iphoneSE_models_choice)
    iphoneSE_model.current(0)
    iphoneSE_model.place(x=85, y=210)

    iphoneSE_storage_choice = ('128GB','64GB')
    iphoneSE_storage = Combobox(canvas,
    state='readonly',
    width=6,
    height=1,
    values=iphoneSE_storage_choice)
    iphoneSE_storage.current(0)
    iphoneSE_storage.place(x=165, y=210)

    iphoneSE_colour_choice = ('White', 'Black', 'Red')
    iphoneSE_colour = Combobox(canvas,
    state='readonly',
    width=10,
    height=1,
    values=iphoneSE_colour_choice)
    iphoneSE_colour.current(0)
    iphoneSE_colour.place(x=235, y=210)

    price_SE = StringVar()
    iphoneSE_price = Label(canvas,
    textvariable =price_SE,
    width=8,
    height=1,
    relief=RAISED).place(x=325,y=210)

    subtract_SE = Button(canvas,
    text = '-',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_SE_sub).place(x=325, y=235)

    quantity_SE_value = IntVar()
    quantity_SE = Entry(canvas,
    text = quantity_SE_value,
    width = 4,
    justify=CENTER,
    relief = SUNKEN).place(x=343, y=238)
    quantity_SE_value.set('0')

    add_SE = Button(canvas,
    text = '+',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_SE_add).place(x=371, y=235)

    #-------------------------------------
    iphone11 = Label(canvas,
    text='Iphone 11',
    width=10,
    height=2,
    relief=RAISED).place(x=5,y=275)

    iphone11_models_choice = ('Normal')
    iphone11_model = Combobox(canvas,
    state='readonly',
    width=8,
    height=1,
    values=iphone11_models_choice)
    iphone11_model.current(0)
    iphone11_model.place(x=85, y=285)

    iphone11_storage_choice = ('128GB','64GB')
    iphone11_storage = Combobox(canvas,
    state='readonly',
    width=6,
    height=1,
    values=iphone11_storage_choice)
    iphone11_storage.current(0)
    iphone11_storage.place(x=165, y=285)

    iphone11_colour_choice = ('Purple', 'Green', 'White', 'Black', 'Red')
    iphone11_colour = Combobox(canvas,
    state='readonly',
    width=8,
    height=1,
    values=iphone11_colour_choice)
    iphone11_colour.current(0)
    iphone11_colour.place(x=235, y=285)

    price_11 = StringVar()
    iphone11_price = Label(canvas,
    textvariable =price_11,
    width=8,
    height=1,
    relief=RAISED).place(x=325,y=285)

    subtract_11 = Button(canvas,
    text = '-',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_11_sub).place(x=325, y=310)

    quantity_11_value = IntVar()
    quantity_11 = Entry(canvas,
    text = quantity_11_value,
    width = 4,
    justify=CENTER,
    relief = SUNKEN).place(x=343, y=313)
    quantity_11_value.set('0')

    add_11 = Button(canvas,
    text = '+',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_11_add).place(x=371, y=310)

    #-------------------------------------
    air_pods = Label(canvas,
    text='Air Pods',
    width=10,
    height=2,
    relief=RAISED).place(x=5,y=350)

    airpod_models_choice = ('Pro', '3rd Generation', '2nd Generation' )
    airpod_model = Combobox(canvas,
    state='readonly',
    width=14,
    height=1,
    values=airpod_models_choice)
    airpod_model.current(0)
    airpod_model.place(x=85, y=360)

    price_airpod = StringVar()
    airpod_price = Label(canvas,
    textvariable =price_airpod,
    width=8,
    height=1,
    relief=RAISED).place(x=325,y=360)

    subtract_airpod = Button(canvas,
    text = '-',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_airpod_sub).place(x=325, y=385)

    quantity_airpod_value = IntVar()
    quantity_airpod = Entry(canvas,
    text = quantity_airpod_value,
    width = 4,
    justify=CENTER,
    relief = SUNKEN).place(x=343, y=388)
    quantity_airpod_value.set('0')

    add_airpod = Button(canvas,
    text = '+',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_airpod_add).place(x=371, y=385)

    #-------------------------------------
    air_pods_max = Label(canvas,
    text='Air Pods Max',
    width=10,
    height=2,
    relief=RAISED).place(x=5,y=425)

    airpodmax_models_choice = ('Max')
    airpodmax_model = Combobox(canvas,
    state='readonly',
    width=8,
    height=1,
    values=airpodmax_models_choice)
    airpodmax_model.current(0)
    airpodmax_model.place(x=85, y=435)

    air_pods_max_colour_choice = ('Space Grey', 'Silver', 'Pink', 'Green', 'Sky Blue')
    airpodmax_colour = Combobox(canvas,
    state='readonly',
    width=10,
    height=1,
    values=air_pods_max_colour_choice)
    airpodmax_colour.current(0)
    airpodmax_colour.place(x=165, y=435)

    price_airpodmax = StringVar()
    airpodmax_price = Label(canvas,
    textvariable =price_airpodmax,
    width=8,
    height=1,
    relief=RAISED).place(x=325,y=435)

    subtract_airpodmax = Button(canvas,
    text = '-',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_airpodmax_sub).place(x=325, y=460)

    quantity_airpodmax_value = IntVar()
    quantity_airpodmax = Entry(canvas,
    text = quantity_airpodmax_value,
    width = 4,
    justify=CENTER,
    relief = SUNKEN).place(x=343, y=463)
    quantity_airpodmax_value.set('0')

    add_airpodmax = Button(canvas,
    text = '+',
    height = 1,
    width = 1,
    relief = RAISED,
    command=quantity_for_airpodmax_add).place(x=371, y=460)

    #-----------------threads to update price---------
    get_price_iphone_13()
    get_price_iphone_12()
    get_price_iphone_SE()
    get_price_iphone_11()
    get_price_airpods()
    get_price_airpods_max()
    root.mainloop()
c_s.close()
