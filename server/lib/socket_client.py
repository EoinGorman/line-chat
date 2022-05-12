import socket

class SocketClient:
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = '!DISCONNECT'

    def __init__(self, conn):
        self.connected = True
        self.socket = conn
        self.conversation = None

    def receive_message(self):
        msg_length = self.socket.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.socket.recv(msg_length).decode(self.FORMAT)
            return msg

    def send_message(self, message):
        msg = message.encode(self.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.socket.send(send_length)
        self.socket.send(msg)

    def get_conversation(self):
        return self.conversation

    def set_conversation(self, conversation):
        self.conversation = conversation

    def get_connected(self):
        return self.connected

    def set_connected(self, value):
        self.connected = value

    def close(self):
        self.set_connected(False)

    def __del__(self):
        self.close()