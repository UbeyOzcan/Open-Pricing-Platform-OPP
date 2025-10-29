import psycopg


class DBConn:
    def __init__(self, username: str, password: str, db:str, host: str, port: int):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = db

    def connect(self):
        conn = psycopg.connect(
            dbname=self.db,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return conn

C = DBConn("postgres", "postgres", "frenchmtpldb", "localhost", "2022")
conn = C.connect()
