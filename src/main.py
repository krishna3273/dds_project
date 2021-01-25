from database import DB
config = {
    "HOST": "10.3.5.211",
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
    db.exec("CREATE TABLE DHF (feagment_id int, relation varchar(255), HF_id int, attribute varchar(255), site_id int)")

def main():
    db = DB(config = config)
    db.connect()
    db.exec("USE Zoo;")
    init_relations(db)
    db.close_cursor()
    db.close_connection()
if __name__ == "__main__" :
    main()
