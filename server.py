import socket
import threading
import os

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accept_connections()

    def accept_connections(self):
        ip = socket.gethostbyname(socket.gethostname())
        port = int(input('Enter desired port --> '))
        self.s.bind((ip, port))
        self.s.listen(100)
        print('Running on IP:', ip)
        print('Running on port:', port)
        while True:
            c, addr = self.s.accept()
            print("Connection from:", addr)
            threading.Thread(target=self.handle_client, args=(c, addr)).start()

    def handle_client(self, c, addr):
        data = c.recv(1024).decode()
        if not os.path.exists(data):
            c.send("file-doesn't-exist".encode())
            c.shutdown(socket.SHUT_RDWR)
            c.close()
        else:
            c.send("file-exists".encode())
            print('Sending', data)
            try:
                with open(data, 'rb') as file:
                    while True:
                        data_chunk = file.read(1024)
                        if not data_chunk:
                            break
                        c.send(data_chunk)
            except Exception as e:
                print("Error occurred while sending:", e)
            finally:
                c.shutdown(socket.SHUT_RDWR)
                c.close()

server = Server()
