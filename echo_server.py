import socket
import sys
import threading

def receive_message(connection):
    data = b""
    while True:
        part = connection.recv(1024)
        data += part
        if len(part) < 1024:
            break
    return data

"""
Function to handle communication with a connected client.
Runs in a separate thread for each client.
"""
def handle_client(connection, client_address):
    try:
        print(f"Connection from {client_address}")
        while True:
            data = receive_message(connection)
            if data:
                message = data.decode()
                print(f"Received from {client_address}: {message}")
                connection.sendall(data)
                break
            else:
                print(f"Connection closed by {client_address}")
                break
    finally:
        connection.close()

"""
Function to start the server, listen for incoming connections, and create a new thread for each connected client.
"""
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', port)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"Server is listening on port {port}...")

    while True:
        connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()
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