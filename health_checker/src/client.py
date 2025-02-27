import logging
import socket
import threading
import time
from typing import Callable

app_logger = logging.getLogger("app")

hello_endpoint_active = True


def health_request(host: str, port: int):
    """30秒周期で/healthリクエストを投げる（接続を使い回す）"""
    app_logger.info("create thread health")
    app_logger.info("create socket for /health request.")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as health_socket:
        health_socket.connect((host, port))
        while hello_endpoint_active:
            health_socket.sendall("/health".encode())
            app_logger.info("message sent")
            response = health_socket.recv(1024)
            app_logger.info(f"Response to /health: {response.decode()}")
            time.sleep(10)


def hello_request(host: str, port: int):
    """10秒周期で/helloリクエストを投げる（毎回接続を作る）"""
    app_logger.info("create thread hello")
    while hello_endpoint_active:
        app_logger.info("create socket for /hello request.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            client_socket.sendall("/hello".encode())
            app_logger.info("message sent")
            response = client_socket.recv(1024)
            app_logger.info(f"Response to /hello: {response}")
            time.sleep(5)
    if not hello_endpoint_active:
        app_logger.info("hello_endpoint_active is False. Stopping the client.")


def start(dest: str, port: int) -> None:
    """クライアントを起動し、スレッドでリクエストを投げ続ける"""
    hello_thread = threading.Thread(target=hello_request,  args=(dest, port))
    hello_thread.daemon = True  # detach
    hello_thread.start()

    health_thread = threading.Thread(target=health_request, args=(dest, port))
    health_thread.daemon = True  # detach
    health_thread.start()

    try:
        while True:
            time.sleep(1)  # サーバー機能の処理は省く
    except KeyboardInterrupt:
        print("クライアントを終了します。")
