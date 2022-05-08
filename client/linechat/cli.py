import requests

import click
import json

import linechat.lib.constants as constants

@click.group
def cli():
    pass

@cli.command()
@click.option("--username", "-u", "username", required=True, help="Username to signup with.")
@click.option("--password", "-p", "password", required=True, help="Password to signup with.")
def signup(username, password):
    data = json.dumps({"username":username, "password":password})
    response = requests.put(f"http://localhost:{constants.SERVER_PORT}/user", data = data)
    #response = requests.post(f"http://localhost:{constants.SERVER_PORT}/login", data = data})
    if response.status_code == 200:
        print("success")
        #     add user to db, set logged_in flag as True
    else:
        print(response.text)

@cli.command()
@click.option("--username", "-u", "username", required=True, help="Username to signup with.")
@click.option("--password", "-p", "password", required=True, help="Password to signup with.")
def login(username, password):
    data = json.dumps({"username":username, "password":password})
    response = requests.post(f"http://localhost:{constants.SERVER_PORT}/user", data = data)
    #response = requests.post(f"http://localhost:{constants.SERVER_PORT}/login", data = data})
    if response.status_code == 200:
        print(response.text)
        #     add user to db, set logged_in flag as True
    else:
        print(response.text)

if __name__ == '__main__':
    cli()
