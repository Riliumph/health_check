import asyncio
import logging
import random

from interactor.context import request_id_var
from log.access_log import RequestIDFilter


async def handle_hello() -> str:
    """ /hello に対するレスポンスを生成 """
    access_logger = logging.getLogger("access")
    access_logger.addFilter(RequestIDFilter(request_id_var.get()))
    wait_time = random.randint(1, 3)
    access_logger.info(f"hello called; wait {wait_time} sec")
    await asyncio.sleep(wait_time)
    return "hello"
