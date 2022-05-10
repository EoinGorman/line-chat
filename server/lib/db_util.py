from configparser import ConfigParser

import psycopg2

class DbUtil:
    def __init__(self):
        self.conn = self.connect()
        self.cur = self.conn.cursor()

    def config(self, filename='./lib/database.ini', section='postgresql'):
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

    def select(self, table, field, value):
        self.execute(f"SELECT * FROM {table} WHERE {field} = '{value}'")
        return self.cur.fetchall()

    def select_all(self, table):
        self.execute(f"SELECT * FROM {table}")
        return self.cur.fetchall()

    def execute(self, command):
        self.cur.execute(command)
        self.conn.commit()

    def close(self):
        self.conn.close()