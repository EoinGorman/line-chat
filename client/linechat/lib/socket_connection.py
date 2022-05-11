from email import message
import socket
import threading

from python_sockets.client import HEADER

class SocketConnection:
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = '!DISCONNECT'

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, conversation_name):
        self.connected = True
        self.client.connect(self.ADDR)
        listener_thread = threading.Thread(target=self.receive_message)
        listener_thread.start()
        self.send_message(conversation_name)
        while self.connected:
            message = input()
            self.send_message(message)

    def send_message(self, message):
        msg = message.encode(self.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def receive_message(self):
        while self.connected:
            msg_length = self.client.recv(HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    self.connected = False
                print(f"{msg}")

    def close(self):
        self.send_message(self.DISCONNECT_MESSAGE)
        self.connected = False

    def __del__(self):
        self.close()