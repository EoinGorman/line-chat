import json
import requests
import sys, os

from flask import Flask, jsonify, request, Response

import lib.constants as constants
from lib.user_manager import UserManager

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/user', methods = ['PUT', 'POST'])
def user():
    params = json.loads(request.get_data().decode("utf-8"))
    user_manager = UserManager(params["username"], params["password"])
    if request.method == 'PUT':
        success, message = user_manager.add_user()
    else:
        success, message = user_manager.login()

    if success:
        message = user_manager.id()
        return Response(f"{message}", status=200)
    else:
        return Response(f"{message}", status=400)

@app.route('/send_message',  methods = ['POST'])
def send_message():
    message = request.get_data().decode("utf-8")
    # talk to db, add message from user to conversation in db
    return 'Sent message: ' + message

@app.route('/get_messages', methods= ['GET'])
def get_messages():
    # talk to db, get all messages for user for a conversation
    return 'messages: '

if __name__ == '__main__':
    app.run(port=constants.SERVER_PORT)
