import pytest

from src.game.board import Board


@pytest.fixture(autouse=True)
def board(settings):
    arena, *_ = settings
    rows, columns, *_ = arena
    return Board(rows, columns)
