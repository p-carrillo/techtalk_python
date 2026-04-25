from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Scene(ABC):
    def __init__(self) -> None:
        self.context: dict[str, Any] = {}

    def set_context(self, context: dict[str, Any]) -> None:
        self.context = context

    @abstractmethod
    def enter(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def exit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_events(self, events: list[Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, delta_time: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError
