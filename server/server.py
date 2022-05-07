import requests
import sys, os
from flask import Flask, jsonify, request

# relative modules
sys.path.append(os.path.join(sys.path[0], '../', 'common'))
import constants

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/register_user')
def register_user():
    return 'registered'

@app.route('/login')
def login():
    return 'logged in'

@app.route('/send_message',  methods = ['POST'])
def send_message():
    message = request.get_data().decode("utf-8")
    return 'Sent message: ' + message

if __name__ == '__main__':
    app.run(port=constants.SERVER_PORT)
