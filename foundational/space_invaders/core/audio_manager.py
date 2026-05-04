from __future__ import annotations


class AudioManager:
    def __init__(self, volume: float = 0.5) -> None:
        self.volume = volume

    def set_volume(self, volume: float) -> None:
        self.volume = max(0.0, min(1.0, volume))

    def play(self, _sound_id: str) -> None:
        # Placeholder extensible: ready for real sound assets.
        return
