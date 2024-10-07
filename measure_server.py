import socket
import sys
import re
import time

# Function to check if the message is a valid setup message.
def check1(message):
    return re.match(r"^s\s(rtt\s([1-9]|10)\s(1|100|200|400|800|1000)|tput\s([1-9]|10)\s(1000|2000|4000|8000|16000|32000))\s(\d+\.?\d*)$", message)

# Function to check if the message is a valid test message.
def check2(message, expected_size, expected_seq):
    actual_size = get_test_datelen(message)
    actual_seq = get_test_seq(message)
    return actual_size == int(expected_size) and actual_seq == expected_seq

# Function to check if the message is a valid test message without sequence number.
def check2_noseq(message):
    list = message.split()
    return len(list) == 3 and int(list[1]) == 0

# Function to check if the message is a valid termination message.
def check3(message):
    return re.match(r"^t$", message)

# Function to get the message size from the setup message.
def get_message_size(message):
    return str(message.split()[3])

# Function to get the number of probes from the setup message.
def get_message_probes(message):
    return int(message.split()[2])

# Function to get the message delay from the setup message.
def get_message_delay(message):
    return float(message.split()[4])

# Function to get the message type from the setup message.
def get_type(message):
    return message.split()[1]

# Function to receive messages from the client.
def receive_message(connection):
    data = b""
    while True:
        part = connection.recv(1024)
        data += part
        if len(part) < 1024:
            break
    return data

# Function to get the sequence number from the test message.
def get_test_seq(str):
    return int(str.split()[1])

# Function to get the data length from the test message.
def get_test_datelen(str):
    return len(str.split()[2])

# Function to start the server, listen for incoming connections, and handle the communication.
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', port)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"Server is listening on port {port}...")

    message_size = 0
    message_type = ""
    message_probes = 0

    setUp = False
    measure = False
    terminate = False

    while True:
        connection, client_address = server_socket.accept()
        try:
            print(f"Connection from {client_address}")
            while True:
                data = receive_message(connection)
                if data:
                    message = data.decode()

                    if check1(message):
                        print("check1 Received: " + message)
                        connection.sendall(b"200 OK\n")
                        message_size = get_message_size(message)
                        message_probes = get_message_probes(message)
                        message_delay = get_message_delay(message)
                        setUp = True

                    elif not check1(message) and setUp == False:
                        print(f"Received not valid setup message: {message}")
                        connection.sendall(b"404 ERROR: Invalid Connection Setup Message")
                        break

                    elif check2_noseq(message):
                        print(f"check2 Received: {message}")
                        for i in range(message_probes):
                            connection.sendall(data)
                            data = receive_message(connection)
                            print(f"repeat Received: {data.decode()}")
                            if check3(data.decode()):
                                connection.sendall(b"200 OK: Closing Connection\n")
                                break
                            if not check3(data.decode()) and i == message_probes - 1:
                                print("3")
                                connection.sendall(b"404 ERROR: Invalid Connection Termination Message\n")
                                break
                            if not check2(data.decode(), message_size, i+1):
                                print("2")
                                connection.sendall(b"404 ERROR: Invalid Measurement Message\n")
                                break
                            time.sleep(message_delay)

                    elif not check2_noseq(message):
                        print(f"Received not valid test message: {message}")
                        connection.sendall(b"404 ERROR: Invalid Measurement Message\n")
                        break

                else:
                    print(f"Connection closed by {client_address}")
                    break

        finally:
            connection.close()
            break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 measure_server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    if 58000 <= port <= 58999:
        start_server(port)
    else:
        print("Please use a port between 58000 and 58999")