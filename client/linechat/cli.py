from urllib import response
import requests
import sys

import click
import json

import linechat.lib.constants as constants
from linechat.lib.db_util import DbUtil
from linechat.lib.socket_connection import SocketConnection

@click.group
def cli():
    pass

@cli.command()
@click.option("--username", "-u", "username", required=True, help="Username to signup with.")
@click.option("--password", "-p", "password", required=True, help="Password to signup with.")
def signup(username, password):
    data = json.dumps({"username":username, "password":password})
    response = requests.put(f"http://localhost:{constants.SERVER_PORT}/user", data = data)
    if response.status_code == 200:
        db = DbUtil()
        rows = db.select_user('username', username)
        if rows == []:
            db.insert_user(int(response.text), username, password)
        db.set_signed_in(username, password)
        print("success")
    else:
        print(response.text)

@cli.command()
@click.option("--username", "-u", "username", required=True, help="Username to signup with.")
@click.option("--password", "-p", "password", required=True, help="Password to signup with.")
def login(username, password):
    data = json.dumps({"username":username, "password":password})
    response = requests.post(f"http://localhost:{constants.SERVER_PORT}/user", data = data)
    if response.status_code == 200:
        user_id = int(response.text)
        db = DbUtil()
        rows = db.select_user('username', username)
        if rows == []:
            db.insert_user(user_id, username)
        db.set_signed_in(user_id)
        print("success")
    else:
        print(response.text)

@cli.command()
def signed_in():
    db = DbUtil()
    rows = db.select_user('signed_in', 1)
    print(f"Currently signed in as {rows[0][1]}")

@cli.command()
def conversations():
    response = requests.get(f"http://localhost:{constants.SERVER_PORT}/conversations")
    if response.status_code == 200:
        print(f"<conversation_id>: <conversation_name>")
        conversations = json.loads(response.text)
        for conv in conversations:
            print(f"{conv[0]}: {conv[1]}")


@cli.command()
@click.option("--name", "-n", "conversation_name", required=True, help="Name of conversation to create.")
def create_conversation(conversation_name):
    db = DbUtil()
    user_id = db.select_user('signed_in', 1)[0][0]
    data = json.dumps({"conversation_name":conversation_name, "user_id":user_id})
    response = requests.put(f"http://localhost:{constants.SERVER_PORT}/conversations", data = data)
    if response.status_code == 200:
        print(f"Created {conversation_name} successfully.")
    else:
        print(f"Failed to create conversation: {conversation_name}.")

@cli.command()
@click.option("--name", "-n", "conversation_name", required=True, help="Name of conversation to join.")
def join_conversation(conversation_name):
    try:
        response = requests.get(f"http://localhost:{constants.SERVER_PORT}/conversations")
        if response.status_code == 200:
            conversations = json.loads(response.text)
            valid_conv = False
            for conv in conversations:
                if conversation_name == conv[1]:
                    valid_conv = True

            if valid_conv:
                sock = SocketConnection()
                sock.connect(conversation_name)
            else:
                print(f"{conversation_name} conversation does not exist.")
        else:
            print(f"Error contacting server for conversations list: {response.text}")
    except KeyboardInterrupt:
        sock.close()
        sys.exit(0)

if __name__ == '__main__':
    cli()
