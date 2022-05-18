import socket
import threading

from applescript import tell


class SocketConnection:
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    HEADER = 64
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = '!DISCONNECT'

    def __init__(self, user_name, conversation_name):
        self.user_name = user_name
        self.conversation_name = conversation_name
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.conversation_log = f"/tmp/linechat-{conversation_name}.log"
        with open(self.conversation_log, 'w') as f:
            f.write(f"---- {conversation_name} chat ----\n")

    def connect(self):
        self.connected = True
        self.client.connect(self.ADDR)

        writing_thread = threading.Thread(target=self.write_messages)
        writing_thread.start()

        reading_thread = threading.Thread(target=self.receive_messages)
        reading_thread.start()

        display_thread = threading.Thread(target=self.tail_conversation)
        display_thread.start()

    def write_messages(self):
        self.send_message(self.user_name)
        self.send_message(self.conversation_name)
        print("Type here to send messages...")
        while self.connected:
            message = input("--> ")
            self.send_message(message)

    def receive_messages(self):
        while self.connected:
            msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MESSAGE:
                    self.connected = False
                else:
                    with open(self.conversation_log, 'a') as f:
                        f.write(f"{msg}\n")

    def tail_conversation(self):
        # open new window to show conversation
        cmd = f"tail -f {self.conversation_log}"
        tell.app('Terminal', 'do script "' + cmd + '"')

    def send_message(self, message):
        msg = message.encode(self.FORMAT)
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(msg)

    def close(self):
        if self.connected:
            self.send_message(self.DISCONNECT_MESSAGE)
        self.connected = False
        #todo delete /tmp file

    def __del__(self):
        print("deleting")
        self.close()
