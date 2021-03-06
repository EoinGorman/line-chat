import socket
import sys
import threading

from socket_client import SocketClient

class SocketConnection:
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = '!DISCONNECT'

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conversations = {}
        self.running = False

    def start(self):
        self.server.bind(self.ADDR)
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}:{self.PORT}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

    def handle_client(self, conn, addr):
        print("Handling client")
        client = SocketClient(conn)
        user_name = client.receive_message() # First message will be user name
        client.set_user(user_name)
        conv_name = client.receive_message() # Second message will be conversation name to join
        client.set_conversation(conv_name)
        print(f"[NEW CONNECTION] New user has joined {conv_name}")

        if conv_name not in self.conversations:
            self.conversations[conv_name] = []
        self.conversations[conv_name].append(client)

        while client.get_connected():
            message = client.receive_message()
            if message == self.DISCONNECT_MESSAGE:
                client.close()
            elif message:
                message = f"{user_name}: {message}"
                self.broadcast_message(message, conv_name)
        print(f"[DISCONNECT] Removing {client} from {conv_name}")
        self.conversations[conv_name].remove(client)

    def broadcast_message(self, message, conversation):
        print(f"[BROADCAST] Sending {message} to {conversation} chat.")
        for client in self.conversations[conversation]:
            print(f"[CLIENT] {client}")
            client.send_message(message)

    def close(self):
        for conversation in self.conversations:
            self.broadcast_message(self.DISCONNECT_MESSAGE, conversation)
        self.connected = False

    def __del__(self):
        self.close()

if __name__ == '__main__':
    try:
        sock = SocketConnection()
        sock.start()
    except KeyboardInterrupt:
        sock.close()
        sys.exit(0)