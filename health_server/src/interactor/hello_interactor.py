import logging

app_logger = logging.getLogger("app")


def handle_hello() -> str:
    """ /hello に対するレスポンスを生成 """
    app_logger.info("hello called")
    return "hello"
