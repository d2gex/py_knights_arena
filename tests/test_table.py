import pytest

from os.path import join
from src.reader import Reader
from src.board import Board
from tests import utils as test_utils


@pytest.fixture
def table_settings():
    reader = Reader()
    return reader.get_game_settings(join(test_utils.TEST, 'stubs', 'game_settings'))


@pytest.fixture(autouse=True)
def board(table_settings):
    arena, *_ = table_settings
    return Board(*arena)


def test_set_knights(board, table_settings):
    '''Ensure nights are placed in the arena as given by their original positions
    '''
    arena, knights, items = table_settings
    board.set_knights(knights)
    red, green = board.knights['RED'], board.knights['GREEN']

    # Check red position
    x, y = knights['RED']['position']
    assert board[x][y][0] == red.name

    # Check green position
    x, y = knights['GREEN']['position']
    assert board[x][y][0] == green.name


def test_set_items(board, table_settings):
    '''Ensure nights are placed in the arena as given by their original positions
    '''
    *_, items = table_settings
    board.set_items(items)
    axe, magic_staff = board.items['Axe'], board.items['MagicStaff']

    # Check red position
    x, y = items['Axe']['position']
    assert board[x][y][0] == axe.name

    # Check green position
    x, y = items['MagicStaff']['position']
    assert board[x][y][0] == magic_staff.name
