import MySQLdb

class MySQL():

    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = db
        self.db = None
        self.cur = None

    def connect(self):
        self.db = MySQLdb.connect(host=self.host, user = self.user, passwd = self.passwd, db = self.database)
        self.cur = self.db.cursor()

    def insert(self, table, msg):
        self.cur.execute("insert into " + table + " values " + "(" + msg + ")")

    def disconnect(self):
        self.db.close()

    def commit(self):
        self.db.commit()

