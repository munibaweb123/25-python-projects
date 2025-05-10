import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.7"
        self.port = 5555
        self.addr = (self.server, self.port)
        # self.id = self.connect()
        self.pos = self.connect() or "Connection failed"

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(f"Connection error: {e}")
            return None


    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def getPos(self):
        return self.pos
n = Network()
print(n.send("Hello World!")) # This will send the string "Hello World!" to the server and print the response.
print(n.send('Working'))