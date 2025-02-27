
from typing import Callable, Dict

from interactor.health import handle_health
from interactor.hello import handle_hello

ROUTE_TABLE: Dict[str, Callable[[], str]] = {
    "/health": handle_health,
    "/hello": handle_hello,
}


async def handle_request(command: str) -> str:
    """リクエストに対する適切なレスポンスを返す"""
    return await ROUTE_TABLE.get(command, lambda: "unknown command")()
