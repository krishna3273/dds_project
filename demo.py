import pymysql
from sshtunnel import SSHTunnelForwarder

HOST = "10.3.5.215"
DATABASE_NAME = "Zoo"
USER = "krishna"
PASSWORD = "iiit123"
PORT = 22
SSH_UNAME = "user"
SSH_PASS = "iiit123"
DB_HOST = "127.0.0.1"

class DB():
    def _init_(self):
        self.cursor = None
        self.conn = None
        pass

    def connect(self):
        tunnel = SSHTunnelForwarder((HOST, PORT), ssh_password=SSH_PASS, ssh_username=SSH_UNAME,
             remote_bind_address=(DB_HOST, 3306))
        tunnel.start()
        conn = pymysql.connect(host='127.0.0.1', user=USER, passwd=PASSWORD, port=tunnel.local_bind_port)
        self.cursor = conn.cursor()
        self.conn = conn

    def exec(self, query):
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        while row is not None:
            print(row)
            row = self.cursor.fetchone()

    def close_cursor(self):
        self.cursor.close()

    def close_connection(self):
        try:
            self.close_cursor()
            self.conn.close()
        except:
            pass

db = DB()
db.connect()
db.exec("SHOW DATABASES;")
db.exec("USE  Zoo;")
db.close_connection()