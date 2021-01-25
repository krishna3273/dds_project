import pymysql
from sshtunnel import SSHTunnelForwarder
from connection import DB
import csv


config={"HOST":"10.3.5.215","DATABASE_NAME":"Zoo",
"USER":"krishna",
"PASSWORD":"iiit123",
"PORT":22,
"SSH_UNAME":"user",
"SSH_PASS":"iiit123",
"DB_HOST":"127.0.0.1"}

db = DB(config)
db.connect()
db.exec("SHOW DATABASES;")
db.exec("USE  Zoo;")
# db.exec("DROP TABLE Accountant;")
# db.exec("CREATE TABLE Doctor (Doctor_id INT,Specialisation varchar(64))")
# db.exec("CREATE TABLE Accountant (Acc_id INT,Record_id INT)")
# db.exec("CREATE TABLE Record (Record_id INT AUTO_INCREMENT,Patient_id INT,Doctor_id INT,Bill INT,Visiting_Date DATETIME DEFAULT NOW(),PRIMARY KEY(Record_id))")

filename="../data/accountant.csv"

fields=[]
rows=[]

with open(filename,'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader) 
    for row in csvreader: 
        rows.append(row)
    print("Total no. of rows: %d"%(csvreader.line_num))


print('Field names are:' + ', '.join(field for field in fields))

# for row in rows: 
    # db.exec(f'INSERT INTO Doctor VALUES({row[0]},"{row[1]}");') 
    # db.exec(f'INSERT INTO Record(Patient_id,Doctor_id,Bill) VALUES({row[0]},{row[1]},{row[2]});') 
#     db.exec(f'INSERT INTO Accountant VALUES({row[0]},{row[1]});') 
#     print(row)
#     db.conn.commit()
# db.exec('DELETE FROM Accountant WHERE Acc_id NOT IN(Select Employee_id FROM Employee);')
# db.conn.commit()
db.close_connection()