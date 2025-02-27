import argparse
import logging

import logger
from server import start

app_logger = logging.getLogger("app")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L4 Server with epoll")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Server host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=84,
                        help="Server port (default: 84)")
    args = parser.parse_args()
    app_logger.info(f"argument: {args.host}:{args.port}")
    start(args.host, args.port)
