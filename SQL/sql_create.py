import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="admin",         # your password
                     db="test")        # name of the data base

cur = db.cursor()

cur.execute("CREATE TABLE DATA("
            "time float,"
            "val float);")

cur.execute("DESCRIBE DATA")

#cur.execute("SELECT * FROM DATA")

# print all the first cell of all the rows
for row in cur.fetchall():
    print (row)

db.close()