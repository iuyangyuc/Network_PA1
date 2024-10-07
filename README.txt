Run Instructions
================
For echo service:
1. Open a terminal and run the server using the command: python3 echo_server.py <port_number>
2. Open another terminal and run the client using the command: python3 echo_client.py <server_ip> <port_number> <message>

notes:
- <port_number> should be an integer between 58000 and 58999
- These two can be run on the same machine or different machines

For measurement service:
========================
1. Open a terminal and run the server using the command: python3 measure_server.py <port>
2. Open another terminal and run the client using the command: python3 measure_client.py <server_ip> <port> <measure> <probes> <size> <delay>
3. Result can be find in rtt.txt or tput.txt

notes:
- <port_number> should be an integer between 58000 and 58999
- <measure> should be either 'rtt' or 'tput'
- limits for <probes>, <size> and <delay> are describe in pdf
- delay is in seconds. Although it can be any number, but larger number is not recommended.
- These two can be run on the same machine or different machines

Trade-off in measuring RTT and throughput
=========================================
1. For displaying received message while measuring and check if received a 404 message, there are extra logic in the code which may affect the RTT and throughput measurement.

