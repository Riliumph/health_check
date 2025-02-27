import logging

from interactor.context import request_id_var
from logger import RequestIDFilter


def handle_hello() -> str:
    """ /hello に対するレスポンスを生成 """
    print("hello called")
    access_logger = logging.getLogger("access")
    access_logger.addFilter(RequestIDFilter(request_id_var.get()))
    access_logger.info("hello called")
    return "hello"
