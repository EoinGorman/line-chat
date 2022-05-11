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
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.running = False

    def start(self):
        self.server.bind(self.ADDR)
        self.server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.listen, args=(conn, addr))
            thread.start()

    def listen(self, conn, addr):
        self.connected = True
        conversation_name = self.receive_message()
        print(f"[NEW CONNECTION] New user has joined {conversation_name}")

        if conversation_name not in self.clients:
            self.clients[conversation_name] = []
        self.clients[conversation_name].append(conn)

        while True: # TODO change  to some var, allow socket to stop listening for client
            message = self.receive_message()
            self.broadcast_message(message, conversation_name)

    def broadcast_message(self, message, conversation):
        msg = message.encode(self.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        for client in self.clients[conversation]: # TODO don't send message back to client who sent it
             client.send(send_length)
             client.send(message)

    def receive_message(self):
        msg_length = self.server.recv(HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.server.recv(msg_length).decode(self.FORMAT)
            if msg == self.DISCONNECT_MESSAGE:
                self.connected = False # TODO make this client specific
            self.broadcast_message(f"{msg}")

    def close(self):
        self.broadcast_message(self.DISCONNECT_MESSAGE)
        self.connected = False

    def __del__(self):
        self.close()