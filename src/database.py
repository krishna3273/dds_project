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
    def __init__(self, config):
        self.cursor = None
        self.conn = None
        self.HOST = config["HOST"]
        self.PORT = config["PORT"]
        self.SSH_PASS = config["SSH_PASS"]
        self.SSH_UNAME = config["SSH_UNAME"]
        self.DB_HOST = config["DB_HOST"]
        self.USER = config["USER"]
        self.PASSWORD = config["PASSWORD"]

    def connect(self):
        tunnel = SSHTunnelForwarder((self.HOST, self.PORT), ssh_password=self.SSH_PASS, ssh_username=self.SSH_UNAME,
             remote_bind_address=(self.DB_HOST, 3306))
        tunnel.start()
        conn = pymysql.connect(host='127.0.0.1', user=self.USER, passwd=self.PASSWORD, port=tunnel.local_bind_port)
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

