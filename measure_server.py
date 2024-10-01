import socket
import sys
import re
import time


def check1(message):
    return re.match(r"^s\s(rtt\s([1-9]|10)\s(1|100|200|400|800|1000)|tput\s([1-9]|10)\s(1000|2000|4000|8000|16000|32000))\s([0-9]{1,3}|1000)$", message)

def check2(message, message_size):
    return re.match( fr"^m\s([1-9]|10)\s{message_size}$", message)

def check3(message):
    return re.match(r"^t$", message)

def get_message_size(message):
    return str(message.split()[3])

def get_message_probes(message):
    return int(message.split()[2])

def get_type(message):
    return message.split()[1]

def rtt_measurement(connection, size, probes):
    list = []
    message = 'a' * size
    for i in range(probes):
        start_time = time.time()
        connection.sendall(message.encode())
        response = connection.recv(1024)
        end_time = time.time()
        rtt = end_time - start_time
        list.append(rtt)
    for i in list:
        print(i)
    return list

def tput_measurement(connection, size, probes):
    message = 'a' * size
    list = []
    for i in range(probes):
        start_time = time.time()
        connection.sendall(message.encode())
        total_data_received = 0
        while total_data_received < size:
            data = connection.recv(1024)
            total_data_received += len(data)
        end_time = time.time()
        tput = total_data_received / (end_time - start_time)  # throughput in bytes per second
        list.append(tput)
    for i in list:
        print(i)
    return list

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
                data = connection.recv(1024)
                if data:
                    message = data.decode()
                    print(f"Received: {message}")

                    if check1(message):
                        connection.sendall(b"200 OK\n")
                        connection.sendall(data)
                        message_size = get_message_size(message)
                        message_type = get_type(message)
                        message_probes = get_message_probes(message)
                        setUp = True

                    if not check1(message) and setUp == False:
                        connection.sendall(b"404 ERROR: Invalid Connection Setup Message")
                        break

                    if check2(message, message_size):
                        measure = True
                        if message_type == "rtt":
                            connection.sendall(b"200 OK: RTT Measurement Complete\n")
                            connection.sendall(data)
                            rtt_list = rtt_measurement(connection, message, message_probes)
                        if message_type == "tput":
                            connection.sendall(b"200 OK: Throughput Measurement Complete\n")
                            connection.sendall(data)

                    if not check1(message) and not check2(message, message_size) and measure == False:
                        connection.sendall(b"404 ERROR: Invalid Measurement Message\n")
                        break


                    if check3(message):
                        connection.sendall(b"200 OK: Closing Connection\n")
                        break

                    if not check1(message) and not check2(message, message_size) and not check3(message) and terminate == False:
                        connection.sendall(b"404 ERROR: Invalid Connection Termination Message\n")
                        break

                else:
                    print(f"Connection closed by {client_address}")
                    break

        finally:
            connection.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python echo_server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    if 58000 <= port <= 58999:
        start_server(port)
    else:
        print("Please use a port between 58000 and 58999")