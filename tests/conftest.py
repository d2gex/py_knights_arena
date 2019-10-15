import pytest

from os.path import join
from src.game.reader import SettingReader
from tests import utils as test_utils


@pytest.fixture(scope='session')
def table_settings():
    reader = SettingReader()
    return reader.get_game_settings(join(test_utils.TEST, 'stubs', 'game_settings'))
