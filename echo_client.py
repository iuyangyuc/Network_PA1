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
Function to receive messages from the server.
Runs in a separate thread.
"""
def receive_messages(client_socket):
    while True:
        try:
            data = receive_message(client_socket)
            if not data:
                print("Connection closed by server.")
                break
            print(f"Received echo: {data.decode()}")
            break
        except ConnectionResetError:
            print("Connection reset by server.")
            break
        except Exception as e:
            print(f"Receive error: {e}")
            break

"""
Function to send messages to the server.
Runs in a separate thread.
"""
def send_messages(client_socket, message):
    while True:
        try:
            client_socket.sendall(message.encode())
            break
        except Exception as e:
            print(f"Send error: {e}")
            break

"""
Function to start the client, connect to the server, and initiate send and receive threads.
"""
def start_client(server_ip, server_port, message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)

    try:
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        send_thread = threading.Thread(target=send_messages, args=(client_socket,), kwargs={"message": message})

        receive_thread.start()
        send_thread.start()

        send_thread.join()
        receive_thread.join()
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python echo_client.py <server_ip> <port> <message>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    message = sys.argv[3]
    if 58000 <= server_port <= 58999:
        start_client(server_ip, server_port, message)
    else:
        print("Please use a port between 58000 and 58999")