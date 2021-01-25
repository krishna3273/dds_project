from connection import DB
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


def main():
    db = DB(config = config)
    db.connect()


if __name__ == "__main__" :
    main()
