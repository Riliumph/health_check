import logging

app_logger = logging.getLogger("app")


def handle_health() -> str:
    """ /health に対するレスポンスを生成 """
    app_logger.info("health called")
    return "healthy"
