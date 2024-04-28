import socket

def main():
    host = socket.gethostname()
    port = 3000
    client_socket = socket.socket()
    client_socket.connect((host, port))
    
    response = client_socket.recv(300000).decode()
    print(response)
    
    client_socket.close()

if __name__ == "__main__":
    main()
