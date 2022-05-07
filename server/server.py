import json
import requests
import sys, os

from flask import Flask, jsonify, request

import lib.constants as constants
from lib.user_manager import UserManager

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/user', methods = ['PUT'])
def user():
    params = json.loads(request.get_data().decode("utf-8"))
    user_manager = UserManager(params["username"], params["password"])
    message = user_manager.add_user()
    return message

@app.route('/login')
def login():
    params = json.loads(request.get_data().decode("utf-8"))
    user_manager = UserManager(params["username"], params["password"])
    message = user_manager.login()
    return message

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
