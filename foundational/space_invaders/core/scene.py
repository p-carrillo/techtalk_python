from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame
    from space_invaders.core.game import Game


class Scene(ABC):
    def __init__(self, game: Game) -> None:
        self.game = game

    @abstractmethod
    def enter(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def exit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, delta_time: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError
