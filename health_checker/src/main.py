import argparse
import asyncio
import logging

from client import client
from server import server

from common.log import logger

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
    logger.init("/app/common/log/config.json")
    app_logger.info(f"argument: {args.host}:{args.port}")
    client.start(args.host, args.port)

    src_host = "0.0.0.0"
    src_port = 84
    asyncio.run(server.start(src_host, src_port))
