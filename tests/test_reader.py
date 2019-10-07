import pytest
import yaml

from os.path import join
from src.reader import Reader
from tests import utils as test_utils


@pytest.fixture(autouse=True)
def settings():
    with open(join(test_utils.TEST, 'stubs', 'game_settings')) as fh:
        return yaml.safe_load(fh)


def test_fetch_setting_data_table(settings):
    reader = Reader()
    table, *_ = reader.fetch_setting_data(settings)

    # a) table should be a tuple
    assert table == (8, 8)


def test_fetch_setting_data_knights(settings):
    '''Ensure knights are dicts and the position is a tuple of two integers
    '''
    reader = Reader()
    table, knights, *_ = reader.fetch_setting_data(settings)

    # --> RED and GREEN knights should be in
    assert all(kns in knights for kns in ('R', 'G'))
    position = knights['R']['position']
    # --> position is a tuple of two integers
    assert all(condition for condition in (len(position) == 2,
                                           isinstance(position, tuple),
                                           all(isinstance(x, int) for x in position)))


def test_fetch_setting_data_items(settings):
    '''Ensure items are dicts and the position is a tuple of two integers
    '''
    reader = Reader()
    *_, items = reader.fetch_setting_data(settings)

    # --> Axe and MagicStaff items should be in
    assert all(item in items for item in ('A', 'M'))
    position = items['A']['position']
    # --> position is a tuple of two integers
    assert all(condition for condition in (len(position) == 2,
                                           isinstance(position, tuple),
                                           all(isinstance(x, int) for x in position)))


def test_get_game_settings():
    '''a tuple with table, knights and dicts should be returned from any file settings
    '''
    reader = Reader()
    table, knights, items = reader.get_game_settings(join(test_utils.TEST, 'stubs', 'game_settings'))
    assert isinstance(table, tuple)
    assert isinstance(knights, dict)
    assert isinstance(items, dict)
