import logging
import socket
import time

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
                # timeout_count = timeout_count+1
                # if timeout_count < 3:
                #     app_logger.info("retry")
                #     continue
                # else:
                #     app_logger.error("timeout retry over")
                #     hello_endpoint_active = False
                #     break
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
            # timeout_count = timeout_count+1
            # if timeout_count < 3:
            #     app_logger.info("hello retry")
            #     continue
            # else:
            #     app_logger.error("hello timeout retry over")
            #     hello_endpoint_active = False
            #     break
    app_logger.info(f"hello_endpoint_active is {hello_endpoint_active}")
