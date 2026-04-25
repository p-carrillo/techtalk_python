from space_invaders.services import LevelService, WaveService


def test_wave_service_progression_increases_difficulty() -> None:
    service = WaveService(difficulty="normal")
    wave_1 = service.get_config(1)
    wave_4 = service.get_config(4)

    assert wave_4.enemy_speed > wave_1.enemy_speed
    assert wave_4.fire_chance_per_second > wave_1.fire_chance_per_second


def test_level_service_moves_to_next_wave() -> None:
    level = LevelService(WaveService())
    assert level.current_wave == 1
    level.next_wave()
    assert level.current_wave == 2
