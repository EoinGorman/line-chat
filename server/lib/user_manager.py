from .db_util import DbUtil

class UserManager:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db = DbUtil()

    def add_user(self):
        message = ''
        if self.user_exists():
            message = f'User {self.username} already exists'
        else:
            self.db.insert_user(self.username, self.password)
            rows = self.db.select_user(self.username)
            message = str(rows[0][0]) # return user_id
        self.db.close()
        return message

    def login(self):
        message = ''
        rows = self.db.select_user(self.username)
        if rows == []:
            message = 'User does not exist'
        elif rows[0][2] == self.password:
            message = str(rows[0][0]) # return user_id
        else:
            message = 'Incorrect password'
        self.db.close()
        return message

    def user_exists(self):
        rows = self.db.select_user(self.username)
        return rows != [] # if no rows returned, user does not exist