import requests
import sys, os
from flask import Flask, request

sys.path.append(os.path.join(sys.path[0], '..', 'common'))
import constants
import lib.user_manager

app = Flask(__name__)

@app.route('/user', methods = ['PUT'])
def user():
    # name
    # password
    
    return 'registered'

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
