import pytest

from os.path import join
from src.reader import Reader
from src.cell_content import ItemFactory, KNIGHT_DROWNED
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


def test_move_knight_no_item_north_and_drown(board, table_settings):
    '''Ensure that when a knight drowns its status and position are both updated. Test of knight without
    item
    '''
    x, y = 0, 0
    table, knights, items = table_settings
    board.set_knights(knights)

    knight_nk = board.knights['G'].nickname
    board[x][y] = {knight_nk}
    board.k_positions[knight_nk] = x, y

    board.move(knight_nk, 'N')

    assert board.knights[knight_nk].status == KNIGHT_DROWNED  # Knight is drowned
    assert board.k_positions[knight_nk] is None  # Position of drowned knight is null
    assert board[x][y] is None  # previous position remains empty if not no items


def test_move_knight__no_item_west_and_drown(board, table_settings):
    '''Ensure that when a knight drowns its status and position are both updated. Test of knight without
    item
    '''
    x, y = 0, 0
    table, knights, items = table_settings
    board.set_knights(knights)

    knight_nk = board.knights['G'].nickname
    board[x][y] = {knight_nk}
    board.k_positions[knight_nk] = x, y

    board.move(knight_nk, 'W')

    assert board.knights[knight_nk].status == KNIGHT_DROWNED
    assert board.k_positions[knight_nk] is None
    assert board[x][y] is None


def test_move_knight__no_item_south_and_drown(board, table_settings):
    '''Ensure that when a knight drowns its status and position are both updated. Test of knight without
    item
    '''
    x, y = 7, 7
    table, knights, items = table_settings
    board.set_knights(knights)

    knight_nk = board.knights['G'].nickname
    board[x][y] = {knight_nk}
    board.k_positions[knight_nk] = x, y

    board.move(knight_nk, 'S')

    assert board.knights[knight_nk].status == KNIGHT_DROWNED
    assert board.k_positions[knight_nk] is None
    assert board[x][y] is None


def test_move_knight__no_item_east_and_drown(board, table_settings):
    '''Ensure that when a knight drowns its status and position are both updated. Test of knight without
    item
    '''
    x, y = 7, 7
    table, knights, items = table_settings
    board.set_knights(knights)

    knight_nk = board.knights['G'].nickname
    board[x][y] = {knight_nk}
    board.k_positions[knight_nk] = x, y

    board.move(knight_nk, 'E')

    assert board.knights[knight_nk].status == KNIGHT_DROWNED
    assert board.k_positions[knight_nk] is None
    assert board[x][y] is None


def test_move_knight_with_item_drown(board, table_settings):
    '''Ensure that when knight with an item drown its status and position is update as well as its item is
    left on the tile he/she was standing
    '''
    x, y = 7, 7
    table, knights, items = table_settings
    board.set_knights(knights)
    board.set_items(items)

    knight_nk = board.knights['G'].nickname
    axe = board.items['A']
    board.knights[knight_nk].item = axe
    board[x][y] = {knight_nk}
    board.k_positions[knight_nk] = x, y

    board.move(knight_nk, 'E')

    assert board.knights[knight_nk].status == KNIGHT_DROWNED
    assert board.k_positions[knight_nk] is None
    assert board[x][y] == {axe.nickname}


def test_move_knight_no_item_to_empty_cell(board, table_settings):
    '''When a knight with no item moves into an empty cell the destination cell should be updated
    '''
    table, knights, items = table_settings
    board.set_knights(knights)

    knight_nk = board.knights['G'].nickname
    x, y = board.k_positions[knight_nk]
    assert board[x][y]
    assert board[x+1][y] is None
    board.move(knight_nk, 'S')

    assert board[x][y] is None  # previous cell is now empty
    assert board[x+1][y] == {knight_nk}  # new cells shows the knight moved
    assert board.k_positions[knight_nk] == (x+1, y)  # the position of the knight needs to be updated


def test_move_knight_with_item_to_empty_cell(board, table_settings):
    '''When a knight moves into an empty cell it takes its item with him/her
    '''
    table, knights, items = table_settings
    board.set_knights(knights)
    board.set_items(items)

    knight_nk = board.knights['G'].nickname
    axe = board.items['A']
    board.knights[knight_nk].item = axe
    x, y = board.k_positions[knight_nk]
    assert board[x][y]
    assert board[x+1][y] is None
    board.move(knight_nk, 'S')

    assert board[x][y] is None  # previous cell is now empty
    assert board[x+1][y] == {knight_nk}  # new cells shows the knight moved
    assert board.k_positions[knight_nk] == (x+1, y)  # the position of the knight needs to be updated
    assert board.i_positions[axe.nickname] == (x+1, y)  # the position of the item needs to be updated


def test_move_knight_no_item_to_single_item_cell(board, table_settings):
    '''When a knight with no item moves into a cell with a single item, this picks it up.
    '''
    table, knights, items = table_settings
    board.set_knights(knights)
    board.set_items(items)

    knight = board.knights['G']
    assert not knight.item
    x, y = board.k_positions[knight.nickname]
    axe = board.items['A']
    board[x+1][y] = {axe.nickname}
    board.move(knight.nickname, 'S')

    assert board[x][y] is None
    assert board[x + 1][y] == {knight.nickname}
    assert board.k_positions[knight.nickname] == (x + 1, y)
    assert board.i_positions[axe.nickname] == (x + 1, y)
    assert knight.item
