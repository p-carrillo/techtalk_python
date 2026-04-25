from __future__ import annotations

from .wave_service import WaveConfig, WaveService


class LevelService:
    def __init__(self, wave_service: WaveService) -> None:
        self._wave_service = wave_service
        self._current_wave = 1

    @property
    def current_wave(self) -> int:
        return self._current_wave

    def current_config(self) -> WaveConfig:
        return self._wave_service.get_config(self._current_wave)

    def next_wave(self) -> WaveConfig:
        self._current_wave += 1
        return self.current_config()

    def reset(self) -> None:
        self._current_wave = 1
