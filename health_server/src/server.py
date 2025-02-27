import asyncio
import logging
import uuid

from interactor.context import request_id_var
from logger import RequestIDFilter
from router import handle_request

app_logger = logging.getLogger("app")

BUFFER_SIZE = 1024


async def receive_event(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)
    access_logger = logging.getLogger("access")
    access_logger.addFilter(RequestIDFilter(request_id))
    addr = writer.get_extra_info('peername')
    access_logger.info(f"new request by {addr}")
    while True:
        access_logger.info("wait command")
        command = await reader.read(BUFFER_SIZE)
        if not command:
            access_logger.error("client closed connection")
            break
        response = await handle_request(command.decode("utf-8").strip())
        access_logger.info(f"response: {response}")
        writer.write(response.encode("utf-8"))
        await writer.drain()  # Flush + wait
    writer.close()
    await writer.wait_closed()
    access_logger.info("connection closed")


async def start(host: str, port: int) -> None:
    server = await asyncio.start_server(receive_event, host, port)
    addr = server.sockets[0].getsockname()
    app_logger.info(f"Server running on {addr}")
    async with server:
        await server.serve_forever()
