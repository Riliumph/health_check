import json
import logging.config
import socket
import time

# ログ設定を定義します
with open('logger.json', 'r') as config_file:
    log_config = json.load(config_file)
logging.config.dictConfig(log_config)
app_logger = logging.getLogger("app")
sys_logger = logging.getLogger("sys")

pre_health = False


def check_health(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            # TODO: 毎回接続するのコスト高い
            s.connect((host, port))

            # ヘルスチェックレスポンスを受け取る
            response = s.recv(1024).decode('utf-8').strip()

            if response == "healthy":
                sys_logger.info("Health check passed.")
                return True
            else:
                sys_logger.error("Unexpected response:", response)
                return False
    except socket.timeout:
        sys_logger.error("Connection timed out.")
        return False
    except socket.error as e:
        sys_logger.error(f"Connection error: {e}")
        return False


if __name__ == "__main__":
    host = "nginx"
    port = 8084
    while True:
        check_health(host, port)
        time.sleep(5)
