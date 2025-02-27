import logging

from interactor.context import request_id_var
from logger import RequestIDFilter


def handle_health() -> str:
    """ /health に対するレスポンスを生成 """
    access_logger = logging.getLogger("access")
    access_logger.addFilter(RequestIDFilter(request_id_var.get()))
    access_logger.info("health called")
    return "healthy"
