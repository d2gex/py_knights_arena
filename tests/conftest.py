import pytest

from os.path import join
from src.app import create_app
from tests.config_test import TestConfig
from tests import utils as test_utils


@pytest.fixture(scope='session')
def settings():
    return test_utils.get_game_settings(join(test_utils.TEST, 'stubs', 'game_settings'))


@pytest.fixture(scope='session', autouse=True)
def app_context():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        yield


@pytest.fixture
def knights_app():
    app = create_app(config_class=TestConfig)
    return app.test_client(use_cookies=True)
