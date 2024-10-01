import socket
import sys
import re
import time

def check1(message):
    return re.match(r"^404.*", message)

def start_client(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)

    try:
        while True:
            message = input("Enter message to send: ")
            client_socket.sendall(message.encode())
            time.sleep(0.3)
            data = client_socket.recv(1024)
            print(f"Received: {data.decode()}")
            if check1(data.decode()) or str(data.decode()) == "200 OK: Closing Connection\n":
                break


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