import pytest
from tests import utils as test_utils


@pytest.fixture(autouse=True)
@test_utils.reset_database(tear='up')
def reset_database():
    '''Reset the database before any test is run
    '''
    yield
