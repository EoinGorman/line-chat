import requests

import click
import json

import linechat.lib.constants as constants
from linechat.lib.db_util import DbUtil

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

if __name__ == '__main__':
    cli()
