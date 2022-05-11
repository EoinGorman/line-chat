import json
from importlib_metadata import method_cache
import requests
import sys, os

from flask import Flask, jsonify, request, Response

import lib.constants as constants
from lib.user_manager import UserManager
from lib.conversation_manager import ConversationManager

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

@app.route('/conversations', methods= ['GET', 'PUT', 'POST'])
def conversations():
    conv_manager = ConversationManager()
    if request.method == 'GET':
        conversations = json.dumps(conv_manager.all_conversations(), default=str)
        return Response(conversations, status=200)
    elif request.method == 'PUT':
        params = json.loads(request.get_data().decode("utf-8"))
        conv_manager.add_conversation(params["conversation_name"], params["user_id"])
        conversation = json.dumps(conv_manager.conversation(params["conversation_name"]), default=str)
        return Response(conversation, 200)

if __name__ == '__main__':
    app.run(port=constants.SERVER_PORT)
