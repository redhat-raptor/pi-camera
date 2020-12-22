import socket
import os
from datetime import datetime
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

def open_connection():
    logging.info('Starting receiver')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", 9000))
    sock.listen(1)
    client, address = sock.accept()
    sock.close()
    return client

def file_transfer(client):
    logging.info('Starting transfer')
    _filename = 'picture-received-{}.jpg'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))
    with open(f'{_filename}.part', 'wb') as outfile:
        while True:
            block = client.recv(1024)
            if not block:
                break
            outfile.write(block)
    os.rename(f'{_filename}.part', _filename)
    logging.info('wrote {} bytes'.format(os.stat(_filename).st_size))

def main():
    while True:
        client = open_connection()
        file_transfer(client)
        client.close()


if __name__ == "__main__":
    main()

