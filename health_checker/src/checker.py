import json
import logging.config
import os
import socket
import time

log_dir = "/app/logs"
os.makedirs(log_dir, exist_ok=True)
with open('logger.json', 'r') as config_file:
    log_config = json.load(config_file)
logging.config.dictConfig(log_config)
app_logger = logging.getLogger("app")
sys_logger = logging.getLogger("sys")

pre_health = False


def check_health(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout) as s:
            # ヘルスチェックレスポンスを受け取る
            response = s.recv(1024)
            if not response:
                sys_logger.error("server closed connection")
                return False
            response = response.decode('utf-8').strip()

            if response == "healthy":
                sys_logger.info("Health check passed.")
                return True
            else:
                sys_logger.error("server application error:", response)
                return False
    except socket.timeout:
        sys_logger.error("Connection timed out.")
        return False
    except socket.error as e:
        sys_logger.error(f"Connection error: {e}")
        return False


if __name__ == "__main__":
    interval = 5
    while True:
        check_health(host="nginx", port=8084, timeout=5)
        time.sleep(interval)
