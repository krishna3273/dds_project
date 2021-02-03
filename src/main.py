from database import DB
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

def init_relations(db):
    db.exec("CREATE TABLE CONFIG (relation_name varchar(255), fragmentation_type int)")
    db.exec("CREATE TABLE HF (fragment_id int, relation varchar (255), attribute varchar(255), op varchar(255), value varchar(255), datatype varchar(255), site_id int, PRIMARY KEY (fragment_id))")
    db.exec("CREATE TABLE SITEINFO (site_id int, ip_address varchar(255), user varchar(255), password varchar(255), PRIMARY KEY (site_id))")
    db.exec("CREATE TABLE VF (fragment_id int, relation varchar(255), attribute varchar(255), site_id int)")
    db.exec("CREATE TABLE METADATA (relation varchar(255), derived_relation varchar(255))")
    db.exec("CREATE TABLE DHF (fragment_id int, relation varchar(255), HF_id int, attribute varchar(255), site_id int)")

def pop_CONFIG(db):
    #CONFIG
    db.exec("ALTER TABLE CONFIG MODIFY fragmentation_type varchar(255)")
    db.exec("INSERT INTO CONFIG VALUES ('Employee', 'HF')")
    db.exec("INSERT INTO CONFIG VALUES ('Doctor', 'DHF')")
    db.exec("INSERT INTO CONFIG VALUES ('Patient', 'VF')")
    db.exec("INSERT INTO CONFIG VALUES ('Accountant', 'DHF')")
    db.exec("INSERT INTO CONFIG VALUES ('Record', 'HF')")

def pop_HF(db):
    #HF
    db.exec("INSERT INTO HF VALUES (1, 'Employee', 'Location', '=', 'Chennai', 'string', 3)")
    db.exec("INSERT INTO HF VALUES (2, 'Employee', 'Location', '=', 'Hyderabad', 'string', 1)")
    db.exec("INSERT INTO HF VALUES (3, 'Employee', 'Location', '=', 'Bangalore', 'string', 2)")
    db.exec("INSERT INTO HF VALUES (4, 'Record', 'Bill', '>=', 1000, 'string', 3)")
    db.exec("INSERT INTO HF VALUES (5, 'Record', 'Bill', '<', 1000, 'string', 2)")

def pop_VF(db):
    db.exec("INSERT INTO VF VALUES (1, 'Patient', 'Patient_id;Name', 1)")
    db.exec("INSERT INTO VF VALUES (2, 'Patient', 'Patient_id;Address;Contact_Number', 2)")

def pop_DHF(db):
    db.exec("INSERT INTO DHF VALUES (1, 'Doctor', 1, 'Doctor_id', 3)")
    db.exec("INSERT INTO DHF VALUES (2, 'Doctor', 2, 'Doctor_id', 1)")
    db.exec("INSERT INTO DHF VALUES (3, 'Doctor', 3, 'Doctor_id', 2)")
    db.exec("INSERT INTO DHF VALUES (4, 'Accountant', 1, 'Acc_id', 3)")
    db.exec("INSERT INTO DHF VALUES (5, 'Accountant', 2, 'Acc_id', 1)")
    db.exec("INSERT INTO DHF VALUES (6, 'Accountant', 3, 'Acc_id', 2)")

def pop_SITEINFO(db):
    db.exec("INSERT INTO SITEINFO VALUES (1, '10.3.5.215', 'krishna', 'iiit123')")
    db.exec("INSERT INTO SITEINFO VALUES (2, '10.3.5.213', 'krishna', 'iiit123')")
    db.exec("INSERT INTO SITEINFO VALUES (3, '10.3.5.211', 'krishna', 'iiit123')")

def pop_METADATA(db):
    db.exec("INSERT INTO METADATA VALUES ('Employee', 'Doctor')")
    db.exec("INSERT INTO METADATA VALUES ('Employee', 'Accountant')")

def pop_all(db):
    pop_CONFIG(db)
    pop_HF(db)
    pop_VF(db)
    pop_DHF(db)
    pop_SITEINFO(db)
    pop_METADATA(db)

def main():
    db = DB(config = config)
    db.connect()
    db.exec("USE Zoo;")
    # init_relations(db)
    pop_all(db)
    db.conn.commit()
    db.close_cursor()
    db.close_connection()
if __name__ == "__main__" :
    main()
