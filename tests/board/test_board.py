import json

from src.game.cell_content import KNIGHT_LIVE, KNIGHT_DEAD, KNIGHT_DROWNED


def test_set_knights(board, settings):
    '''Ensure nights are placed in the arena as given by their original positions
    '''
    arena, knights, items = settings
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


def test_set_items(board, settings):
    '''Ensure knights are placed in the arena as given by their original positions
    '''
    *_, items = settings
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


def test_to_json_knight_structure(board, settings):
    '''Ensure that all entries in the return dictionaries are lists. In the case for knight there should
    be 5 elements and for items 2
    '''
    table, knights, items = settings
    board.set_knights(knights)
    board.set_items(items)
    data = json.loads(board.to_json())
    assert all(isinstance(value, list) and len(value) == 5 for key, value in data.items() if key in ('red', 'green'))
    assert all(isinstance(value, list) and len(value) == 2 for key, value in data.items()
               if key in ('axe', 'helmet', 'magic_staff'))


def test_to_json_knight_position(board, settings):
    '''Ensure the knight position is reported as a list of integers
    '''
    table, knights, items = settings
    board.set_knights(knights)
    board.set_items(items)
    data = json.loads(board.to_json())
    assert data['red'][0] == [3, 5]


def test_to_json_knight_status(board, settings):
    '''Ensure the knight status is LIVE, DEAD or DROWNED depending on the case
    '''
    table, knights, items = settings
    board.set_knights(knights)
    board.set_items(items)
    red = board.knights['R']

    # When alive the status is LIVE
    data = json.loads(board.to_json())
    assert data['red'][1] == KNIGHT_LIVE

    # When alive the status is DROWNED
    red.status = KNIGHT_DROWNED
    data = json.loads(board.to_json())
    assert data['red'][1] == KNIGHT_DROWNED

    # When alive the status is DEAD
    red.status = KNIGHT_DEAD
    data = json.loads(board.to_json())
    assert data['red'][1] == KNIGHT_DEAD


def test_to_json_knight_item(board, settings):
    '''Ensure the knight item is either null or whatever item they have at the time
    '''
    table, knights, items = settings
    board.set_knights(knights)
    board.set_items(items)
    red = board.knights['R']

    # When no item => null
    data = json.loads(board.to_json())
    assert data['red'][2] is None

    # When alive the status is DROWNED
    axe = board.items['A']
    red.item = axe
    data = json.loads(board.to_json())
    assert data['red'][2] == axe.name


def test_to_json_knight_attack_score(board, settings):
    '''Ensure the knight's attack score shows its value taking into account the item if it has it
    '''
    table, knights, items = settings
    board.set_knights(knights)
    board.set_items(items)
    red = board.knights['R']

    data = json.loads(board.to_json())
    assert data['red'][3] == 1

    axe = board.items['A']
    red.item = axe
    data = json.loads(board.to_json())
    assert data['red'][3] == 3


def test_to_json_knight_defence_score(board, settings):
    '''Ensure the knight's defence score shows its value taking into account the item if it has it
    '''
    table, knights, items = settings
    board.set_knights(knights)
    board.set_items(items)
    red = board.knights['R']

    data = json.loads(board.to_json())
    assert data['red'][3] == 1

    magic_staff = board.items['M']
    red.item = magic_staff
    data = json.loads(board.to_json())
    assert data['red'][3] == 2


def test_to_json_item_position(board, settings):
    '''Ensure the item position is reported as a list of integers
    '''
    table, knights, items = settings
    board.set_knights(knights)
    board.set_items(items)
    data = json.loads(board.to_json())
    assert data['axe'][0] == [6, 5]


def test_to_json_item_usage(board, settings):
    '''Ensure the item position is reported as a list of integers
    '''
    table, knights, items = settings
    board.set_knights(knights)
    board.set_items(items)
    data = json.loads(board.to_json())
    assert data['axe'][1] is False

    red = board.knights['R']
    axe = board.items['A']
    red.item = axe
    data = json.loads(board.to_json())
    assert data['axe'][1] is True
