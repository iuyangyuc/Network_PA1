import socket
import sys
import re
import time

# Function to check if the message is a 404 error.
def check1(message):
    return re.match(r"^404.*", message)

# Function to check if the message is a 200 OK.
def check2(message):
    return re.match(r"^200.*", message)

# Function to receive messages from the server.
def receive_message(connection):
    data = b""
    while True:
        part = connection.recv(1024)
        data += part
        if len(part) < 1024:
            break
    return data

# Function to build the first message.
def build_message1(measure, probes, size, delay):
    return f"s {measure} {probes} {size} {delay}\n"

# Function to build the second message.
def build_message2(sequence_number, size):
    payload = "A" * int(size)
    return f"m {sequence_number} {payload}\n"

# Function to build the third message.
def build_message3():
    return "t\n"

# Function to measure RTT.
def measure_rtt(client_socket, size, probes):
    print("Measuring RTT...")
    file = open("rtt.txt", "w")
    for i in range(probes):
        start = time.time()
        client_socket.sendall(build_message2(i, size).encode())
        data = receive_message(client_socket)
        print("RTT Received: " + data.decode())
        if check1(data.decode()):
            print(data.decode())
            break
        end = time.time()
        rtt = end - start
        print(f"RTT: {rtt}")
        file.write(f"{rtt}\n")

# Function to measure TPUT based on RTT.
def measure_tput(client_socket, size, probes):
    print("Measuring TPUT...")
    file = open("tput.txt", "w")
    for i in range(probes):
        start = time.time()
        client_socket.sendall(build_message2(i, size).encode())
        data = receive_message(client_socket)
        print(f"TPUT Received: {data.decode()}")
        if check1(data.decode()):
            print(data.decode())
            break
        end = time.time()
        rtt = end - start
        print(f"RTT: {size / rtt}")
        file.write(f"{size / rtt}\n")


# Function to start the client, connect to the server, and initiate send and receive threads.
def start_client(server_ip, server_port, measure, probes, size, delay):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (server_ip, server_port)
    client_socket.connect(server_address)
    message1 = build_message1(measure, probes, size, delay)

    try:
        while True:
            # Phase1
            client_socket.sendall(message1.encode())
            print(f"Sent: {message1}")
            data = receive_message(client_socket)
            message = data.decode()
            if check2(message):
                print(f"Phase1 Received: {data.decode()}")
            else:
                print(f"Phase1 Received: {data.decode()}")
                break


            # Phase2
            if measure == "rtt":
                measure_rtt(client_socket, int(size), int(probes))

            if measure == "tput":
                measure_tput(client_socket, int(size), int(probes))

            # Phase3
            client_socket.sendall(build_message3().encode())
            data = receive_message(client_socket)
            message = data.decode()
            if check1(message):
                print(data.decode())
                break
            else:
                print(data.decode())
                break

            break

    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python3 measure_client.py <server_ip> <port> <measure> <probes> <size> <delay>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    measure = sys.argv[3]
    probes = sys.argv[4]
    size = sys.argv[5]
    delay = sys.argv[6]

    if 58000 <= server_port <= 58999:
        start_client(server_ip, server_port, measure, probes, size, delay)
    else:
        print("Please use a port between 58000 and 58999")