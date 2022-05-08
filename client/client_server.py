import requests
import sys, os

from flask import Flask, request

import lib.constants

app = Flask(__name__)

@app.route('/user', methods = ['PUT', 'POST'])
def user():
    # params: name, password
    params = json.loads(request.get_data().decode("utf-8"))
    data = {"username":params["username"], "password":params["password"]}
    if request.method == 'PUT':
        response = requests.post(f"http://localhost:{constants.SERVER_PORT}/add_user", data = data})
    else:
        response = requests.post(f"http://localhost:{constants.SERVER_PORT}/login", data = data})
    # if success:
    #     add user to db, set logged_in flag as True
    # else:
    #     do nothing, just return error message

    return 'success'

@app.route('/send_message', methods = ['POST'])
def send_message():
    message = request.get_data().decode("UTF-8")
    response = requests.post(f'http://localhost:{constants.SERVER_PORT}/send_message', data = message)
    return 'Sending message: ' + response.text

@app.route('/get_messages', methods = ['GET'])
def get_messages():
    response = requests.post(f'http://localhost:{constants.SERVER_PORT}/get_messages', data = {})
    return 'Got message: ' + message

if __name__ == '__main__':
    app.run(port=constants.CLIENT_SERVER_PORT)
