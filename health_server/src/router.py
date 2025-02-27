
from typing import Callable, Dict

from interactor.health_interactor import handle_health
from interactor.hello_interactor import handle_hello

ROUTE_TABLE: Dict[str, Callable[[], str]] = {
    "/health": handle_health,
    "/app": handle_hello,
}


def handle_request(request: str) -> str:
    """リクエストに対する適切なレスポンスを返す"""
    return ROUTE_TABLE.get(request, lambda: "unknown command")()
