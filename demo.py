from mysql.connector import  (connection)
# import mysql.connector as connector
HOST="10.3.5.215"
DATABASE_NAME="Zoo"
USER="krishna"
PASSWORD="iiit123"
db_connection = connection.MySQLConnection(host=HOST, database=DATABASE_NAME, user=USER, password=PASSWORD)
# db_connection = connector.connect(host=HOST, database=DATABASE_NAME, user=USER, password=PASSWORD)
# print("Connected to:", db_connection.get_server_info())