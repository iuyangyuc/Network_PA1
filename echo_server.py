import socket
import sys

def start_server(port):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', port)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"Server is listening on port {port}...")

    while True:
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address}")
            while True:
                data = connection.recv(1024)
                if data:
                    message = data.decode()
                    print(f"Received: {message}")
                    if message.lower() == 'exit':
                        print(f"Client {client_address} has disconnected by sending 'exit'.")
                        break
                    connection.sendall(data)
                else:
                    print(f"Connection closed by {client_address}")
                    break

        finally:
            connection.close()
        break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python echo_server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    if 58000 <= port <= 58999:
        start_server(port)
    else:
        print("Please use a port between 58000 and 58999")