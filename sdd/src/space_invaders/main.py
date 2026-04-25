from __future__ import annotations


def main() -> None:
    try:
        from space_invaders.core.game import Game
    except ModuleNotFoundError as exc:
        if exc.name == "pygame":
            raise SystemExit("pygame is required. Install with: pip install pygame") from exc
        raise

    game = Game()
    game.run()


if __name__ == "__main__":
    main()
