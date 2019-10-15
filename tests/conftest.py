import pytest

from os.path import join
from tests import utils as test_utils


@pytest.fixture(scope='session')
def settings():
    return test_utils.get_game_settings(join(test_utils.TEST, 'stubs', 'game_settings'))
