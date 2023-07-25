import socket
import os

class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()

    def connect_to_server(self):
        self.target_ip = input('Enter server IP: ')
        self.target_port = input('Enter server port: ')
        self.s.connect((self.target_ip, int(self.target_port)))
        self.main()

    def reconnect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.target_ip, int(self.target_port)))

    def main(self):
        while True:
            file_name = input('Enter the file name on the server: ')
            self.s.send(file_name.encode())
            confirmation = self.s.recv(1024)
            if confirmation.decode() == "file-doesn't-exist":
                print("The file doesn't exist on the server.")
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()
            else:
                write_name = 'from_server ' + file_name
                if os.path.exists(write_name):
                    os.remove(write_name)
                with open(write_name, 'wb') as file:
                    while True:
                        data = self.s.recv(1024)
                        if not data:
                            break
                        file.write(data)
                print(file_name, 'was successfully downloaded.')
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.reconnect()

client = Client()
