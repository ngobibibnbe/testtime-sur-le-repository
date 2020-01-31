import os
import socket
import threading
from time import sleep

import hydra

files_dir = os.path.dirname(os.path.realpath(__file__))

class Transfer:
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self, host, port, peer_address=None, peer_port=None, files_list=None, remote_files_list=None):
        self.mysocket.bind((host, port))
        print(' Server is ready ..')
        self.mysocket.listen(5)
        self.remote_files_list = remote_files_list
        self.files_list = files_list

        self.peer = (peer_address, peer_port)
        conn, addr = self.mysocket.accept()

        file_name = conn.recv(2048).decode('utf-8')

        send_thread = threading.Thread(
            target=self.forward_file, args=(file_name, conn))
        send_thread.start()

    def forward_file(self, file_name, conn):
        with open(os.path.join(files_dir,file_name), 'rb') as f:
            data = f.read(1024)
            conn.send(data)
            while data:
                conn.send(data)
                data = f.read(1024)

        if file_name in self.remote_files_list:
            mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mysocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            mysocket.connect(self.peer)

            mysocket.send(file_name.encode('utf-8'))
            while True:
                print('receiving data...')
                data = mysocket.recv(1024)
                print(data)
                if not data:
                    print('break')
                    break
                conn.send(data)

        conn.close()


@hydra.main(config_path='config.yaml')
def app(cfg):
    print(cfg.pretty())
    host, port = cfg.server.address, cfg.server.port
    peer_address, peer_port = cfg.peer.address, cfg.peer.port
    files_list = cfg.files_list.split(',')
    remote_files_list = cfg.remote_files_list.split(',')

    Transfer(host, port, peer_address, peer_port,
             files_list, remote_files_list)

    print(remote_files_list)

if __name__ == "__main__":
    app()
