import pytest

from os.path import join
from src.reader import SettingReader
from src.board import Board
from tests import utils as test_utils


@pytest.fixture
def table_settings():
    reader = SettingReader()
    return reader.get_game_settings(join(test_utils.TEST, 'stubs', 'game_settings'))


@pytest.fixture(autouse=True)
def board(table_settings):
    arena, *_ = table_settings
    rows, columns, *_ = arena
    return Board(rows, columns)
