from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict

EventCallback = Callable[..., None]


class EventBus:
    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, list[EventCallback]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: EventCallback) -> None:
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: EventCallback) -> None:
        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def publish(self, event_name: str, **payload: object) -> None:
        for callback in self._subscribers[event_name]:
            callback(**payload)
