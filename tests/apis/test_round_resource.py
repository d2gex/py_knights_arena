import pytest

from src.apis.namespaces.round import RoundResource
from src import models
from src.app import db


@pytest.fixture(scope='module')
def resource():
    return RoundResource()


def test_round_context_storing_board_size(settings, resource):
    '''Round table should be used to store data about the size of the board
    '''

    table, *_ = settings
    game_data = {'rows': table[0], 'columns': table[1], 'knights': {}}
    resource.create_round(game_data)
    db_data = db.session.query(models.Round).one()
    assert db_data.rows, db_data.columns == (game_data['rows'], game_data['columns'])


def test_round_context_storing_knights(settings, resource):
    '''Settings tables should be used to store data about knights
    '''

    table, knights, __ = settings
    knight_list = []
    for nickname, data in knights.items():
        x, y = data['position']
        data['x'], data['y'] = x, y
        del data['position']
        data['nickname'] = nickname
        knight_list.append(data)
        game_data = {'rows': table[0], 'columns': table[1], 'knights': knight_list}
    print(game_data)
