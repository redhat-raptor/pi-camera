import socket

is_ready = True

def _open_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9000))
    return sock

def send(file_binary):
    is_ready = False

    # Change the following 4 lines and replace with rx/tx communication
    sock = _open_socket()
    sock.sendall(file_binary)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

    is_ready = True
