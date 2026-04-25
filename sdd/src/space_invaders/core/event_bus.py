from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, DefaultDict, List


EventHandler = Callable[[dict[str, Any]], None]


class EventBus:
    def __init__(self) -> None:
        self._listeners: DefaultDict[str, List[EventHandler]] = defaultdict(list)

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._listeners[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: EventHandler) -> None:
        if event_name not in self._listeners:
            return
        self._listeners[event_name] = [h for h in self._listeners[event_name] if h != handler]

    def publish(self, event_name: str, payload: dict[str, Any] | None = None) -> None:
        payload = payload or {}
        for handler in tuple(self._listeners.get(event_name, ())):
            handler(payload)

    def clear(self) -> None:
        self._listeners.clear()
