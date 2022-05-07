import requests
import sys, os

sys.path.append(os.path.join(sys.path[0], '..', 'common'))
import constants

class UserManager:
    def __init__(username, password):
        self.username = username
        self.password = password

    def user_exists():
        # call to main server checking for user in DB
        response = request.get(f'http://localhost:{constants.SERVER_PORT}/user', data = { 'username': self.username, 'password': self.password })