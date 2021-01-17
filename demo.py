from mysql.connector import  connection
import mysql.connector
from sshtunnel import SSHTunnelForwarder

HOST = "10.3.5.215"
DATABASE_NAME = "Zoo"
USER = "krishna"
PASSWORD = "iiit123"
PORT = 22

SSH_UNAME = "user"
SSH_PASS = "iiit123"
DB_HOST = "127.0.0.1"

tunnel = SSHTunnelForwarder(('10.3.5.215', PORT), ssh_password=SSH_PASS, ssh_username=SSH_UNAME,
     remote_bind_address=(DB_HOST, 3306))
tunnel.start()
conn = mysql.connector.connect(host='127.0.0.1', user=USER, passwd=PASSWORD, port=tunnel.local_bind_port)
cur = conn.cursor(buffered=True)
cur.execute("SHOW DATABASES;")
row = cur.fetchone()
while row is not None:
    print(row)
    row = cur.fetchone()
cur.close()
conn.close()