import socket

def open_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9000))
    return sock

def transfer_file(sock, path):
    f = open(path, "rb").read()
    sock.sendall(f)

def main():
    sock = open_socket()
    path = '../picture.jpg' 
    transfer_file(sock, path)
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()

if __name__ == "__main__":
    main()
