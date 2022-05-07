import psycopg2
from configparser import ConfigParser

class DbUtil:
    def __init__(self):
        self.conn = self.connect()
        self.cur = self.conn.cursor()

    def config(self, filename='database.ini', section='postgresql'):
        parser = ConfigParser()
        parser.read(filename)
        db = {}

        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f'Section {section} not found in file {filename}')

        return db

    def connect(self):
        params = self.config()
        return psycopg2.connect(**params)

    def select_user(self, username):
        self.execute(f"SELECT * FROM users WHERE username = '{username}'")
        return self.cur.fetchall()

    def insert_user(self, username, password):
        self.execute(f"INSERT INTO users(username, password, created_at) VALUES ('{username}', '{password}', NOW())")

    def execute(self, command):
        self.cur.execute(command)
        self.conn.commit()

    def close(self):
        self.conn.close()