import pytest

from src.game.board import Board


@pytest.fixture(autouse=True)
def board(table_settings):
    arena, *_ = table_settings
    rows, columns, *_ = arena
    return Board(rows, columns)
