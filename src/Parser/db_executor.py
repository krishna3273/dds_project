import pymysql

class DB():
    def __init__(self, config):
        self.cursor = None
        self.conn = None
        self.USER = config["USER"]
        self.PASSWORD = config["PASSWORD"]

    def connect(self):
        conn = pymysql.connect(host='127.0.0.1', user=self.USER, passwd=self.PASSWORD)
        self.cursor = conn.cursor()
        self.conn = conn

    def exec_fetch(self, query):
        # self.cursor.execute(query)
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