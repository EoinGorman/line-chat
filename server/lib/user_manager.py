from .db_util import DbUtil

class UserManager:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db = DbUtil()

    def add_user(self):
        message = (False, '')
        if self.user_exists():
            message = (False, f'User {self.username} already exists')
        else:
            self.insert_user()
            rows = self.db.select('users', 'username', self.username)
            message = (True, 'success')
        return message

    def login(self):
        message = (False, '')
        rows = self.db.select('users', 'username', self.username)
        if rows == []:
            message = (False, 'User does not exist')
        elif rows[0][2] == self.password:
            message = (True, 'success')
        else:
            message = (False, 'Incorrect password')
        return message

    def id(self):
        rows = self.db.select('users', 'username', self.username)
        return rows[0][0]

    def user_exists(self):
        rows = self.db.select('users', 'username', self.username)
        return rows != [] # if no rows returned, user does not exist

    def insert_user(self):
        self.db.execute(f"INSERT INTO users(username, password, created_at) VALUES ('{self.username}', '{self.password}', NOW())")

    def __del__(self):
        print("user_manager destroyed")
        self.db.close()