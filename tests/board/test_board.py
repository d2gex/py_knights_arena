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
