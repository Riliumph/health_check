import logging
import threading
import time

from client.interactor.health import *

app_logger = logging.getLogger("app")
stop_event = threading.Event()


def start(dest: str, port: int) -> None:
    """クライアントを起動し、スレッドでリクエストを投げ続ける"""
    hello_thread = threading.Thread(target=hello_request,  args=(dest, port))
    hello_thread.daemon = True  # detach
    hello_thread.start()

    health_thread = threading.Thread(target=health_request, args=(dest, port))
    health_thread.daemon = True  # detach
    health_thread.start()

    try:
        while not stop_event.wait(timeout=1):
            pass
    except KeyboardInterrupt:
        print("クライアントを終了します。")
