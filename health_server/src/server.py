import argparse
import json
import logging.config
import os
import selectors
import socket
from typing import Tuple

log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)
with open('logger.json', 'r') as config_file:
    log_config = json.load(config_file)
logging.config.dictConfig(log_config)
app_logger = logging.getLogger("app")
sys_logger = logging.getLogger("sys")

backlog_size = 5
event_handler = selectors.DefaultSelector()


def handle_request(data: str) -> str:
    if data == "/health":
        return "healthy"
    elif data == "/app":
        return "hello"
    return "unknown command"


def accept(server_sock: socket.socket) -> None:
    client_fd, from_info = server_sock.accept()
    app_logger.info(f"Connected by {from_info}")
    client_fd.setblocking(False)
    event_handler.register(client_fd, selectors.EVENT_READ, handle_client)


def handle_client(server_sock: socket.socket) -> None:
    try:
        data = server_sock.recv(1024).decode("utf-8").strip()
        if data:
            response = handle_request(data)
            server_sock.sendall(response.encode("utf-8"))
        else:
            event_handler.unregister(server_sock)
            server_sock.close()
    except ConnectionResetError:
        app_logger.error("Connection reset by peer")
        event_handler.unregister(server_sock)
        server_sock.close()


def start_server(host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(backlog_size)
        server_sock.setblocking(False)
        event_handler.register(server_sock, selectors.EVENT_READ, accept)
        app_logger.info(f"Server listening on {host}:{port}")

        while True:
            events = event_handler.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L4 Server with epoll")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Server host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=84,
                        help="Server port (default: 84)")
    args = parser.parse_args()
    start_server(args.host, args.port)
