import requests
import sys, os
from flask import Flask, jsonify, request

# relative modules
sys.path.append(os.path.join(sys.path[0], '../', 'common'))
import constants
import lib.user_manager as um

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/user', methods = ['PUT'])
def user():
    params = 
    user_manager = um.UserManager()
    message = user_manager.add_user()

@app.route('/login')
def login():
    return 'logged in'

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
