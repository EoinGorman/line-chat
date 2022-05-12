import socket
import sys
import threading


class SocketConnection:
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    HEADER = 64
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
        print("Type to send message...")
        while self.connected:
            message = input()
            self.send_message(message)

    def send_message(self, message):
        msg = message.encode(self.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(msg)

    def receive_message(self):
        while self.connected:
            msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    self.connected = False
                print(f"{msg}")

    def close(self):
        if self.connected:
            self.send_message(self.DISCONNECT_MESSAGE)
        self.connected = False

    def __del__(self):
        print("deleting")
        self.close()

if __name__ == '__main__':
    try:
        sock = SocketConnection()
        sock.connect('miami')
    except KeyboardInterrupt:
        sock.close()
        sys.exit(0)