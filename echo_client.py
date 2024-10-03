import socket
import sys

def receive_message(connection):
    data = b""
    while True:
        part = connection.recv(1024)
        data += part
        if len(part) < 1024:
            break
    return data

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)

    try:
        while True:
            message = input("Enter message to send (type 'exit' to close): ")
            client_socket.sendall(message.encode())
            if message.lower() == 'exit':
                print("Exiting the client...")
                break
            data = receive_message(client_socket)
            print(f"Received echo: {data.decode()}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python echo_client.py <server_ip> <port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    if 58000 <= server_port <= 58999:
        start_client(server_ip, server_port)
    else:
        print("Please use a port between 58000 and 58999")