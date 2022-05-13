import os
import sqlite3

from configparser import ConfigParser

class DbUtil:
    def __init__(self):
        self.conn = self.connect()
        self.cur = self.conn.cursor()

    def config(self, section='sqlite'):
        file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "database.ini")
        parser = ConfigParser()
        parser.read(file)
        db = {}

        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f'Section {section} not found in file {file}')

        return db

    def connect(self):
        db_name = self.config()["database"]
        db_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", f"{db_name}")
        return sqlite3.connect(db_file)

    def select_user(self, field, value):
        self.execute(f"SELECT * FROM users WHERE {field} = '{value}'")
        return self.cur.fetchall()

    def insert_user(self, user_id, username):
        self.execute(f"INSERT INTO users(id, username, signed_in) VALUES ('{user_id}', '{username}', 0)")

    def set_signed_in(self, user_id):
        self.execute(f"UPDATE users SET signed_in = 0 WHERE id != {user_id}")
        self.execute(f"UPDATE users SET signed_in = 1 WHERE id = {user_id}")
        return self.cur.fetchall()

    def logged_in(self):
        pass

    def execute(self, command):
        self.cur.execute(command)
        self.conn.commit()

    def close(self):
        self.conn.close()