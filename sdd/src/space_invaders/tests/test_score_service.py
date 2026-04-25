from space_invaders.services import ScoreService


def test_score_add_and_reset() -> None:
    score = ScoreService()
    assert score.score == 0
    assert score.add(10) == 10
    assert score.add(5) == 15

    score.reset()
    assert score.score == 0
