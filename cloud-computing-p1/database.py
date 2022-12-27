#-------------- database code --------------
# in this file we have some functions to connect,insert,show, and update our database

import pymysql

def database_setup(mode):
   timeout = 10
   connection = pymysql.connect(
   charset="utf8mb4",
   connect_timeout=timeout,
   cursorclass=pymysql.cursors.DictCursor,
   db="defaultdb",
   host="cloud-computing-hw1-maeede-1430.aivencloud.com",
   password="AVNS_3H1sgrF7-Yubx4Ie2fd",
   read_timeout=timeout,
   port=11286,
   user="avnadmin",
   write_timeout=timeout,
   )
   cursor = connection.cursor()
   if mode == 1:
      # we dont have database
      cursor.execute("DROP TABLE ads")

   cursor.execute("CREATE TABLE ads(id int primary key AUTO_INCREMENT, description VARCHAR(255), email VARCHAR(255), state VARCHAR(255) DEFAULT 'in progress', category VARCHAR(255) DEFAULT 'Not identified') ")

   cursor.execute("SHOW TABLES")
   for x in cursor:
      print(x)
   return [cursor,connection]

def database_connection():
   timeout = 10
   connection = pymysql.connect(
   charset="utf8mb4",
   connect_timeout=timeout,
   cursorclass=pymysql.cursors.DictCursor,
   db="defaultdb",
   host="cloud-computing-hw1-maeede-1430.aivencloud.com",
   password="AVNS_3H1sgrF7-Yubx4Ie2fd",
   read_timeout=timeout,
   port=11286,
   user="avnadmin",
   write_timeout=timeout,
   )
   cursor = connection.cursor()
   return [cursor,connection]

def database_insert(cursor, connection, des ,email, state, cat):
   sql = "INSERT INTO ads (description, email, state, category) VALUES (%s, %s, %s, %s)"
   val = (des,email,state,cat)
   cursor.execute(sql, val)
   connection.commit()

def database_show_all(cursor):
   cursor.execute("SELECT * FROM ads")
   myresult = cursor.fetchall()
   counter = 0
   for x in myresult:
      counter = counter + 1
      print(x)
   return counter

def database_get_data(cursor,id):
   empty = 0
   sql = "SELECT * FROM ads Where id = %s"
   val = (id)
   cursor.execute(sql, val)
   myresult = cursor.fetchall()
   if len(myresult) == 0:
      empty = 1
      return empty,None
      
   # id int, description VARCHAR(255), email VARCHAR(255), state VARCHAR(255) , category VARCHAR(255)
   return empty,myresult[0]


def database_update(cursor,connection,id,category,state):
   sql = "UPDATE ads SET state = %s, category = %s WHERE %s = id"
   val = (state,category,id)
   cursor.execute(sql, val)
   connection.commit()
   print("databse updated")
   database_show_all(cursor)

def database_get_email(cursor,id):
   empty = 0
   sql = "SELECT email FROM ads Where id = %s"
   val = (id)
   cursor.execute(sql, val)
   myresult = cursor.fetchall()

   return myresult[0]
