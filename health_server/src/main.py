import argparse
import asyncio
import logging

from server import server

from common.log import logger

app_logger = logging.getLogger("app")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L4 Server with epoll")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Server host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=84,
                        help="Server port (default: 84)")
    args = parser.parse_args()
    logger.init("/app/common/log/config.json")
    app_logger.info(f"argument: {args.host}:{args.port}")
    asyncio.run(server.start(args.host, args.port))
