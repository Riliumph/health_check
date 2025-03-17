import logging
import threading
import time

from client.interactor.health import *

app_logger = logging.getLogger("app")


def start(dest: str, port: int) -> None:
    """クライアントを起動し、スレッドでリクエストを投げ続ける"""
    health_thread = threading.Thread(target=health_request, args=(dest, port))
    health_thread.daemon = True  # detach
    health_thread.start()
