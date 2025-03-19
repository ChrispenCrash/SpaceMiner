import socket
import pickle

class Network:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print("Connected to server")

    def send(self, data):
        self.client.sendall(pickle.dumps(data))
        print(f"Sent data: {data}")

    def receive(self):
        data = pickle.loads(self.client.recv(4096))
        print(f"Received data: {data}")
        return data