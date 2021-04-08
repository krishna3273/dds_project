from Executor.database import DB
from populate import *
from Parser.parse import Parser

config = {
    "HOST": "10.3.5.215",
    "DATABASE_NAME": "Zoo",
    "USER": "krishna",
    "PASSWORD": "iiit123",
    "PORT": 22,
    "SSH_UNAME": "user",
    "SSH_PASS": "iiit123",
    "DB_HOST": "127.0.0.1",
}

def populate(db):
    db.connect()
    db.exec("USE Zoo;")
    pop_all(db)
    db.conn.commit()
    db.close_cursor()
    db.close_connection()

def main():
    db = DB(config = config)
    parser = Parser(config, None)
    sql_test = "SELECT E.Lname FROM EMPLOYEE E, WORKS_ON W, PROJECT P WHERE P.Pname = 'Aquarius' AND P.Pnumber = W.Pno AND E.Ssn=W.Ssn AND E.Bdate = '1957-12-31'"
    sql2 = "select Position from staff, branch where (NOT(Position= 'manager') AND (Position='manager' OR Position='assistant') AND NOT(Position='assistant')OR(BID=SID AND Name='Ali')) "
    # sql3 = "INSERT INTO METADATA VALUES ('Employee', 'Doctor')"
    sql3 = "SELECT EMP.Ename FROM EMP, ASG, PROJ WHERE PROJ.PNO=ASG.PNO AND PROJ.PNAME = 'Instrumentation' AND EMP.ENO = ASG.ENO"
    sql1 = "SELECT * FROM PROJ, ASG WHERE PROJ.PNO=ASG.PNO AND PROJ.PNO='P4'"
    parser.parse(sql_test)
if __name__ == "__main__" :
    main()
