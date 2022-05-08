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
            self.db.insert_user(self.username, self.password)
            rows = self.db.select_user(self.username)
            message = (True, 'success')
        return message

    def login(self):
        message = (False, '')
        rows = self.db.select_user(self.username)
        if rows == []:
            message = (False, 'User does not exist')
        elif rows[0][2] == self.password:
            message = (True, 'success')
        else:
            message = (False, 'Incorrect password')
        return message

    def id(self):
        rows = self.db.select_user(self.username)
        return rows[0][0]

    def user_exists(self):
        rows = self.db.select_user(self.username)
        return rows != [] # if no rows returned, user does not exist

    def __del__(self):
        print("user_manager destroyed")
        self.db.close()