import json
import logging.config
import os
import selectors
import socket

log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)
with open('logger.json', 'r') as config_file:
    log_config = json.load(config_file)
logging.config.dictConfig(log_config)
app_logger = logging.getLogger("app")
sys_logger = logging.getLogger("sys")

HOST = "0.0.0.0"
PORT = 84


def handle_request(data: str) -> str:
    if data == "/health":
        return "healthy"
    elif data == "/app":
        return "hello"
    return "unknown command"


def accept(sock, sel):
    conn, addr = sock.accept()
    app_logger.info(f"Connected by {addr}")
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, handle_client)


def handle_client(conn, sel):
    try:
        data = conn.recv(1024).decode("utf-8").strip()
        if data:
            response = handle_request(data)
            conn.sendall(response.encode("utf-8"))
        else:
            sel.unregister(conn)
            conn.close()
    except ConnectionResetError:
        app_logger.error("Connection reset by peer")
        sel.unregister(conn)
        conn.close()


sel = selectors.DefaultSelector()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    server_sock.setblocking(False)
    sel.register(server_sock, selectors.EVENT_READ, accept)
    app_logger.info(f"Server listening on {HOST}:{PORT}")

    while True:
        events = sel.select()
        for key, _ in events:
            callback = key.data
            callback(key.fileobj, sel)
