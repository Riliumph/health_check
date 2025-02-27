import logging
import selectors
import socket

from router import handle_request

app_logger = logging.getLogger("app")

BACKLOG_SIZE = 5
BUFFER_SIZE = 1024
event_handler = selectors.DefaultSelector()


def accept_event(server_sock: socket.socket) -> None:
    client_fd, from_info = server_sock.accept()
    app_logger.info(f"Connected by {from_info}")
    client_fd.setblocking(False)
    event_handler.register(client_fd, selectors.EVENT_READ, receive_event)


def receive_event(server_sock: socket.socket) -> None:
    try:
        app_logger.info(f"new request: {request}")
        request = server_sock.recv(BUFFER_SIZE).decode("utf-8").strip()
        if not request:
            app_logger.error("client closed connection")
            event_handler.unregister(server_sock)
            server_sock.close()
            return

        response = handle_request()
        server_sock.sendall(response.encode("utf-8"))
    except ConnectionResetError:
        app_logger.error("Connection reset by peer")
        event_handler.unregister(server_sock)
        server_sock.close()
    except Exception as e:
        app_logger.error(f"Error: {e}")
        event_handler.unregister(server_sock)
        server_sock.close()


def start(host: str, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((host, port))
        server_sock.listen(BACKLOG_SIZE)
        server_sock.setblocking(False)
        event_handler.register(server_sock, selectors.EVENT_READ, accept_event)
        app_logger.info(f"Server listening on {host}:{port}")

        while True:
            events = event_handler.select()
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)
