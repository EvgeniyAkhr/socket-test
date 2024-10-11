import json
import sys
import socket
import time
import threading

if len(sys.argv) != 4:
    print("Run: python3 client.py <client_id> <host> <port>")
    sys.exit(1)

CLIENT_ID = sys.argv[1] # Current client's id
HOST = sys.argv[2]  # The server's hostname or IP address
PORT = int(sys.argv[3])  # The port used by the server
counter = 0

def listen_to_server(sock: socket.socket) -> None:
    while True:
        data = sock.recv(1024)
        print(data.decode())
        message = json.loads(data.decode())

        if message["client_id"] == CLIENT_ID:
            continue
        t_diff = abs(int(time.time() * 1000) - float(message["timestamp"]))
        if not t_diff:
            continue
        print(f"Message from {message['client_id']}: "
              f"Diff timestamps {t_diff} ms, counter {message['counter']}")

def send_to_server(sock: socket.socket) -> None:
    global counter
    while True:
        time_now_ms = int(time.time() * 1000)
        message = {
            'client_id': CLIENT_ID,
            'timestamp': time_now_ms,
            'counter': counter
        }
        sock.sendall(json.dumps(message).encode())
        counter += 1
        time.sleep(1)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # Receive
    listen_thread = threading.Thread(target=listen_to_server, args=(s,))
    listen_thread.start()
    # Send
    send_to_server(s)
