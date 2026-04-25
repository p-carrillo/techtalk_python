from space_invaders.core.event_bus import EventBus


def test_event_bus_publish_subscribe() -> None:
    bus = EventBus()
    received = []

    def _handler(payload: dict[str, object]) -> None:
        received.append(payload)

    bus.subscribe("score_changed", _handler)
    bus.publish("score_changed", {"score": 99})

    assert received == [{"score": 99}]
