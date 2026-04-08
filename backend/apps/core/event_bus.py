from collections import defaultdict
from typing import Any, Callable

EventHandler = Callable[[dict[str, Any]], None]
_subscribers: dict[str, list[EventHandler]] = defaultdict(list)


def subscribe(event_name: str, handler: EventHandler) -> None:
    _subscribers[event_name].append(handler)


def publish(event_name: str, payload: dict[str, Any]) -> None:
    for handler in _subscribers.get(event_name, []):
        handler(payload)
