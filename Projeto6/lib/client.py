from socket import socket, AF_INET, SOCK_DGRAM
from socket import timeout
import json

class Client():
    def __init__(self, ip, port):
        self.server_address = (ip, port)
        self.socket = socket(family=AF_INET, type=SOCK_DGRAM)
        self.socket.settimeout(0.3)

    def connect(self):
        try:
            data = {"id":0}
            self.socket.sendto(json.dumps(data).encode('utf-8'), self.server_address)
            data = self.socket.recv(4096)
            response = json.loads(data)
        except timeout:
            print("Server Time Out")
            return None
        return response

    def send(self, ident, direction):
        try:
            data = {"id":ident, "direction":direction}
            self.socket.sendto(json.dumps(data).encode('utf-8'), self.server_address)
            data = self.socket.recv(4096)
            response = json.loads(data)
        except timeout:
            print("Server Time Out")
        return response

def __main():
    client = Client('localhost', 8000)
    print(client.connect())

if __name__ == '__main__':
    __main()