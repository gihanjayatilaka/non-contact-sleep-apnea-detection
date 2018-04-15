import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="temp")        # name of the data base

cur = db.cursor()

# Use all the SQL you like

try:
    cur.execute("CREATE TABLE DATA")
except:
    print("Table doesn't exist")

cur.execute("SELECT * FROM DATA")

# print all the first cell of all the rows
for row in cur.fetchall():
    print (row[0])

db.close()