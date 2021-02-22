from database import DB
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
    parser = Parser(config)
    parser.parse("select losition from staff, branch where (NOT(b.Position= 'manag') AND (b.Position='manager' OR b.Position='assistant') AND NOT(b.Position='assistant')OR(b.BID=s.SID AND s.Name='Ali')) ")
if __name__ == "__main__" :
    main()
