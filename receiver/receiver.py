# Ref: https://stackoverflow.com/questions/40822492/make-file-after-receive-bytes-from-client

import socket
import os

def open_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 9000))
    sock.listen(1)
    client, address = sock.accept()
    sock.close()
    return client

def file_transfer(client):
    with open('picture-received.jpg.part', 'wb') as outfile:
        while True:
            block = client.recv(1024)
            if not block:
                break
            outfile.write(block)
    os.rename('picture-received.jpg.part', 'picture-received.jpg')
    print ('wrote', os.stat('picture-received.jpg').st_size, 'bytes')

def main():
    client = open_connection()
    file_transfer(client)
    client.close()



if __name__ == "__main__":
    main()

