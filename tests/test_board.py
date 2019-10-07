import pytest

from os.path import join
from src.reader import Reader
from src.cell_content import KNIGHT_DROWNED
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
    red, green = board.knights['R'], board.knights['G']

    # Check red position
    x, y = knights['R']['position']
    assert red.nickname in board[x][y]
    assert board.k_positions[red.nickname] == (x, y)

    # Check green position
    x, y = knights['G']['position']
    assert green.nickname in board[x][y]
    assert board.k_positions[green.nickname] == (x, y)


def test_set_items(board, table_settings):
    '''Ensure nights are placed in the arena as given by their original positions
    '''
    *_, items = table_settings
    board.set_items(items)
    axe, magic_staff = board.items['A'], board.items['M']

    # Check red position
    x, y = items['A']['position']
    assert axe.nickname in board[x][y]
    assert board.i_positions[axe.nickname] == (x, y)

    # Check green position
    x, y = items['M']['position']
    assert magic_staff.nickname in board[x][y]
    assert board.i_positions[magic_staff.nickname] == (x, y)


def test_move_knight_north_and_drown(board, table_settings):
    table, knights, items = table_settings
    board.set_knights(knights)
    x, y = 0, 0
    board[x][y] = {'G'}
    board.k_positions['G'] = x, y

    # G in (0, 2) drowns if move North
    x, y = board.k_positions['G']
    board.move('G', 'N')

    assert board.knights['G'].status == KNIGHT_DROWNED
    assert board.k_positions['G'] is None
    assert board[x][y] is None


def test_move_knight_west_and_drown(board, table_settings):
    table, knights, items = table_settings
    board.set_knights(knights)
    x, y = 0, 0
    board[x][y] = {'G'}
    board.k_positions['G'] = x, y

    # G in (0, 2) drowns if move North
    x, y = board.k_positions['G']
    board.move('G', 'W')

    assert board.knights['G'].status == KNIGHT_DROWNED
    assert board.k_positions['G'] is None
    assert board[x][y] is None


def test_move_knight_south_and_drown(board, table_settings):
    table, knights, items = table_settings
    board.set_knights(knights)
    x, y = 7, 7
    board[x][y] = {'G'}
    board.k_positions['G'] = x, y

    # G in (0, 2) drowns if move North
    x, y = board.k_positions['G']
    board.move('G', 'S')

    assert board.knights['G'].status == KNIGHT_DROWNED
    assert board.k_positions['G'] is None
    assert board[x][y] is None


def test_move_knight_east_and_drown(board, table_settings):
    table, knights, items = table_settings
    board.set_knights(knights)
    x, y = 7, 7
    board[x][y] = {'G'}
    board.k_positions['G'] = x, y

    # G in (0, 2) drowns if move North
    x, y = board.k_positions['G']
    board.move('G', 'E')

    assert board.knights['G'].status == KNIGHT_DROWNED
    assert board.k_positions['G'] is None
    assert board[x][y] is None
