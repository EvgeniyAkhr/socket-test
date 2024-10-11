import asyncio
import socket
import subprocess
import time
import os

loop = asyncio.get_event_loop()

counter = 0
clients = set()

async def handle_client(conn: socket.socket) -> None:
    print(f"Client connected: {conn.getpeername()}")
    global clients
    clients.add(conn)
    print(f"Amount of connected clients: {len(clients)}")
    while True:
        await asyncio.sleep(1)
        data = await loop.sock_recv(conn, 1024)
        if not data:
            clients.remove(conn)
            print(f"Amount of connected clients: {len(clients)}")
            break

        # Send message to all client except sender
        message = data.decode('utf-8')
        print(message)
        for client_conn in clients:
            if client_conn != conn:
                try:
                    await loop.sock_sendall(client_conn, message.encode() + b'\n')
                except:
                    clients.remove(client_conn)
                    print(f"Amount of connected clients: {len(clients)}")


async def run_server() -> None:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 0))
    s.listen(5)
    s.setblocking(False)

    host, port = s.getsockname()
    print('Listening on {}:{}'.format(host, port))

    while True:
        print('Waiting for connection...')
        conn, addr = await loop.sock_accept(s)
        loop.create_task(handle_client(conn))

loop.run_until_complete(run_server())
