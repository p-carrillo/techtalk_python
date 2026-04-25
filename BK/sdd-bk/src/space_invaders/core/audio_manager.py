from __future__ import annotations


class AudioManager:
    def __init__(self, master_volume: float = 0.5) -> None:
        self.master_volume = max(0.0, min(1.0, master_volume))

    def set_master_volume(self, volume: float) -> None:
        self.master_volume = max(0.0, min(1.0, volume))

    def play_effect(self, _name: str) -> None:
        # Hook point for real sound effects. Kept no-op for minimal asset-less build.
        return
