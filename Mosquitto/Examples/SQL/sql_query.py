import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="admin",  # your password
                     db="test")        # name of the data base

cur = db.cursor()

# Use all the SQL you like

try:
    cur.execute("SELECT * FROM DATA")
except:
    print("Table doesn't exist")


# print all the first cell of all the rows
for row in cur.fetchall():
    print (row)

db.close()