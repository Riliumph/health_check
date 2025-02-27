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
    # timeout_count = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as health_socket:
        app_logger.info("connect to /health")
        health_socket.connect((host, port))
        while hello_endpoint_active:
            try:
                health_socket.sendall("/health".encode())
                app_logger.info("message sent")
                health_socket.settimeout(2)
                response = health_socket.recv(1024)
                app_logger.info(f"Response to /health: {response.decode()}")
                time.sleep(5)
            except socket.timeout:
                app_logger.error("Timeout occurred.")
    app_logger.info(f"hello_endpoint_active is {hello_endpoint_active}")


def hello_request(host: str, port: int):
    """10秒周期で/helloリクエストを投げる（毎回接続を作る）"""
    app_logger.info("create thread hello")
    while hello_endpoint_active:
        try:
            app_logger.info("create socket for /hello request.")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                client_socket.sendall("/hello".encode())
                app_logger.info("message sent")
                client_socket.settimeout(2)
                response = client_socket.recv(1024)
                app_logger.info(f"Response to /hello: {response}")
                time.sleep(10)
        except socket.timeout:
            app_logger.error("Timeout occurred.")
    app_logger.info(f"hello_endpoint_active is {hello_endpoint_active}")


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
