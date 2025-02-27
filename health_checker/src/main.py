import argparse
import logging

import logger
from client import start

app_logger = logging.getLogger("app")

if __name__ == "__main__":
    # コマンドライン引数のパーサー設定
    parser = argparse.ArgumentParser(description="client")
    parser.add_argument('--host', type=str, default='health_server',
                        help='サーバーホスト（デフォルト: health_server）')
    parser.add_argument('--port', type=int, default=80,
                        help='サーバーポート（デフォルト: 84）')
    args = parser.parse_args()

    # クライアントを起動
    start(args.host, args.port)
