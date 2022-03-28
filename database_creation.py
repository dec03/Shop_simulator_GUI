import mysql.connector

mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=''
)

#this is used to naviagte and interact with the database
mycursor = mydb.cursor()


#------------------CREATION OF DATABASE--------------------
#THIS WAS used to create a database/schema called shopkeeper
#mycursor.execute('CREATE DATABASE shopkeeper')
#mycursor.execute('SHOW DATABASES')




#----------------CREATION OF TABLE ONE--------------------------
#this creates a table authentication accounts to check who is allowed to log in to the server
#the attributes in the table being used is username, password, and account_num as a primary key
#mycursor.execute("CREATE TABLE authentication_accounts (account_num INT(4) PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

#-----------------------INSERTION OF DATA INTO TABLE ONE----------
#this inserts data into the authentication_accounts which can be used to sign in to access the server gui.
#query = '''INSERT INTO authentication_accounts (account_num, username, password)
#           VALUES (1000,"John123", "John321"),(2000,"Daniel456", "Daniel654"),(3000,"David789", "David987")'''

#this exectues the commands to insert
#mycursor.execute(query)
#this commits to the database
#mydb.commit()

#-------------RETIEVES DATA FROM FIRST TABLE--------------------
#query
#mycursor.execute("SELECT * FROM authentication_accounts")
#stores all the records of data in variable myresult (list)
#server_accounts = mycursor.fetchall()
#outputs results
#for x in server_accounts:
#  print(x)







#----------------CREATION OF TABLE TWO--------------------------
#this creates a table stock to store a collection of records about products that are sold
#the attributes in the table being used is product_num as the primary key, name, model,
#storage, colour, price, and stock_num
#mycursor.execute("""CREATE TABLE stock (product_num INT(6) PRIMARY KEY, name VARCHAR(255),
#                model VARCHAR(255), storage VARCHAR(255), colour VARCHAR(255), price FLOAT(8), stock_num INT(6))""")

#-----------------------INSERTION OF DATA INTO TABLE TWO----------
#this inserts data into the stock

"""
query =  INSERT INTO stock (product_num, name, model, storage, colour, price, stock_num)
            VALUES
            (100000, 'Iphone 13', 'Pro Max', '128GB', 'Sierra Blue', 1049.00, 13),
            (100001, 'Iphone 13', 'Pro Max', '128GB', 'Silver', 1049.00, 24),
            (100002, 'Iphone 13', 'Pro Max', '128GB', 'Graphite', 1049.00, 53),
            (100003, 'Iphone 13', 'Pro Max', '128GB', 'Gold', 1049.00, 23),
            (100004, 'Iphone 13', 'Pro Max', '256GB', 'Sierra Blue', 1149.00, 0),
            (100005, 'Iphone 13', 'Pro Max', '256GB', 'Silver', 1149.00, 12),
            (100006, 'Iphone 13', 'Pro Max', '256GB', 'Graphite', 1149.00, 5),
            (100007, 'Iphone 13', 'Pro Max', '256GB', 'Gold', 1149.00, 67),
            (100008, 'Iphone 13', 'Pro Max', '512GB', 'Sierra Blue', 1349.00, 52),
            (100009, 'Iphone 13', 'Pro Max', '512GB', 'Silver', 1349.00, 19),
            (100010, 'Iphone 13', 'Pro Max', '512GB', 'Graphite', 1349.00, 0),
            (100011, 'Iphone 13', 'Pro Max', '512GB', 'Gold', 1349.00, 0),
            (100012, 'Iphone 13', 'Pro Max', '1TB', 'Sierra Blue', 1549.00, 23),
            (100013, 'Iphone 13', 'Pro Max', '1TB', 'Silver', 1549.00, 36),
            (100014, 'Iphone 13', 'Pro Max', '1TB', 'Graphite', 1549.00, 0),
            (100015, 'Iphone 13', 'Pro Max', '1TB', 'Gold', 1549.00, 7),

            (100016, 'Iphone 13', 'Pro', '128GB', 'Sierra Blue', 949.00, 0),
            (100017, 'Iphone 13', 'Pro', '128GB', 'Silver', 949.00, 24),
            (100018, 'Iphone 13', 'Pro', '128GB', 'Graphite', 949.00, 31),
            (100019, 'Iphone 13', 'Pro', '128GB', 'Gold', 949.00, 11),
            (100020, 'Iphone 13', 'Pro', '256GB', 'Sierra Blue', 1049.00, 0),
            (100021, 'Iphone 13', 'Pro', '256GB', 'Silver', 1049.00, 59),
            (100022, 'Iphone 13', 'Pro', '256GB', 'Graphite', 1049.00, 7),
            (100023, 'Iphone 13', 'Pro', '256GB', 'Gold', 1049.00, 34),
            (100024, 'Iphone 13', 'Pro', '512GB', 'Sierra Blue', 1249.00, 0),
            (100025, 'Iphone 13', 'Pro', '512GB', 'Silver', 1249.00, 10),
            (100026, 'Iphone 13', 'Pro', '512GB', 'Graphite', 1249.00, 0),
            (100027, 'Iphone 13', 'Pro', '512GB', 'Gold', 1249.00, 53),
            (100028, 'Iphone 13', 'Pro', '1TB', 'Sierra Blue', 1449.00, 4),
            (100029, 'Iphone 13', 'Pro', '1TB', 'Silver', 1449.00, 23),
            (100030, 'Iphone 13', 'Pro', '1TB', 'Graphite', 1449.00, 0),
            (100031, 'Iphone 13', 'Pro', '1TB', 'Gold', 1449.00, 3),

            (100032, 'Iphone 12', 'Mini', '64GB', 'Purple', 579.00, 2),
            (100033, 'Iphone 12', 'Mini', '64GB', 'Blue', 579.00, 42),
            (100034, 'Iphone 12', 'Mini', '64GB', 'Green', 579.00, 45),
            (100035, 'Iphone 12', 'Mini', '64GB', 'White', 579.00, 16),
            (100036, 'Iphone 12', 'Mini', '64GB', 'Black', 579.00, 64),
            (100037, 'Iphone 12', 'Mini', '64GB', 'Red', 579.00, 0),
            (100038, 'Iphone 12', 'Mini', '128GB', 'Purple', 629.00, 0),
            (100039, 'Iphone 12', 'Mini', '128GB', 'Blue', 629.00, 4),
            (100040, 'Iphone 12', 'Mini', '128GB', 'Green', 629.00, 5),
            (100041, 'Iphone 12', 'Mini', '128GB', 'White', 629.00, 56),
            (100042, 'Iphone 12', 'Mini', '128GB', 'Black', 629.00, 24),
            (100043, 'Iphone 12', 'Mini', '128GB', 'Red', 629.00, 29),
            (100044, 'Iphone 12', 'Mini', '256GB', 'Purple', 729.00, 25),
            (100045, 'Iphone 12', 'Mini', '256GB', 'Blue', 729.00, 4),
            (100046, 'Iphone 12', 'Mini', '256GB', 'Green', 729.00, 5),
            (100047, 'Iphone 12', 'Mini', '256GB', 'White', 729.00, 0),
            (100048, 'Iphone 12', 'Mini', '256GB', 'Black', 729.00, 24),
            (100049, 'Iphone 12', 'Mini', '256GB', 'Red', 729.00, 29),

            (100050, 'Iphone 12', 'Normal', '64GB', 'Purple', 679.00, 5),
            (100051, 'Iphone 12', 'Normal', '64GB', 'Blue', 679.00, 6),
            (100052, 'Iphone 12', 'Normal', '64GB', 'Green', 679.00, 2),
            (100053, 'Iphone 12', 'Normal', '64GB', 'White', 679.00, 41),
            (100054, 'Iphone 12', 'Normal', '64GB', 'Black', 679.00, 23),
            (100055, 'Iphone 12', 'Normal', '64GB', 'Red', 679.00, 15),
            (100056, 'Iphone 12', 'Normal', '128GB', 'Purple', 729.00, 63),
            (100057, 'Iphone 12', 'Normal', '128GB', 'Blue', 729.00, 86),
            (100058, 'Iphone 12', 'Normal', '128GB', 'Green', 729.00, 54),
            (100059, 'Iphone 12', 'Normal', '128GB', 'White', 729.00, 0),
            (100060, 'Iphone 12', 'Normal', '128GB', 'Black', 729.00, 98),
            (100061, 'Iphone 12', 'Normal', '128GB', 'Red', 729.00, 6),
            (100062, 'Iphone 12', 'Normal', '256GB', 'Purple', 829.00, 82),
            (100063, 'Iphone 12', 'Normal', '256GB', 'Blue', 829.00, 1),
            (100064, 'Iphone 12', 'Normal', '256GB', 'Green', 829.00, 5),
            (100065, 'Iphone 12', 'Normal', '256GB', 'White', 829.00, 0),
            (100066, 'Iphone 12', 'Normal', '256GB', 'Black', 829.00, 2),
            (100067, 'Iphone 12', 'Normal', '256GB', 'Red', 829.00, 9),

            (100068, 'Iphone SE', 'Normal', '64GB', 'White', 389.00, 82),
            (100069, 'Iphone SE', 'Normal', '64GB', 'Black', 389.00, 1),
            (100070, 'Iphone SE', 'Normal', '64GB', 'Red', 389.00, 5),
            (100071, 'Iphone SE', 'Normal', '128GB', 'White', 429.00, 0),
            (100072, 'Iphone SE', 'Normal', '128GB', 'Black', 429.00, 2),
            (100073, 'Iphone SE', 'Normal', '128GB', 'Red', 429.00, 9),

            (100074, 'Iphone 11', 'Normal', '64GB', 'Purple', 489.00, 7),
            (100075, 'Iphone 11', 'Normal', '64GB', 'Green', 489.00, 61),
            (100076, 'Iphone 11', 'Normal', '64GB', 'Yellow', 489.00, 22),
            (100077, 'Iphone 11', 'Normal', '64GB', 'White', 489.00, 4),
            (100078, 'Iphone 11', 'Normal', '64GB', 'Black', 489.00, 53),
            (100079, 'Iphone 11', 'Normal', '64GB', 'Red', 489.00, 0),
            (100080, 'Iphone 11', 'Normal', '128GB', 'Purple', 539.00, 5),
            (100081, 'Iphone 11', 'Normal', '128GB', 'Green', 539.00, 6),
            (100082, 'Iphone 11', 'Normal', '128GB', 'Yellow', 539.00, 0),
            (100083, 'Iphone 11', 'Normal', '128GB', 'White', 539.00, 41),
            (100084, 'Iphone 11', 'Normal', '128GB', 'Black', 539.00, 0),
            (100085, 'Iphone 11', 'Normal', '128GB', 'Red', 539.00, 15),

            (100086, 'Air Pods', '2nd Generation', 'None', 'White', 119.00, 41),
            (100087, 'Air Pods', '3rd Generation', 'None', 'White', 169.00, 0),
            (100088, 'Air Pods', 'Pro', 'None', 'White', 239.00, 15),

            (100089, 'Air Pods', 'Max', 'None', 'Space Grey', 549.00, 7),
            (100090, 'Air Pods', 'Max', 'None', 'Silver', 549.00, 0),
            (100091, 'Air Pods', 'Max', 'None', 'Pink', 549.00, 0),
            (100092, 'Air Pods', 'Max', 'None', 'Green', 549.00, 4),
            (100093, 'Air Pods', 'Max', 'None', 'Sky Blue', 549.00, 0)
"""
#this exectues the commands to insert
#mycursor.execute(query)
#this commits to the database
#mydb.commit()

#-------------RETRIEVES DATA FROM SECOND TABLE--------------------
#query
#mycursor.execute("SELECT * FROM stock")
#stores all the records of data in variable myresult (list)
#stock_in = mycursor.fetchall()
#outputs results
#for x in stock_in:
#  print(x)
