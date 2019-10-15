from unittest.mock import patch
from tests import utils as test_utils


def test_reset_database():
    '''Test that reset_database works as follows:

    1) When tear='up' => the generator is only consumed once and before foo executes.
    2) When tear='down' => the generator is only consumed once and after bar executes.
    2) When tear='up_down' => the generator is consumed twice, before and after foo_bar.

    '''

    tables = test_utils.all_models
    with patch.object(test_utils.db.session, 'query') as qy_model:
        with patch.object(test_utils.db.session, 'commit'):

            # (1)
            @test_utils.reset_database(tear='up', db_models=tables)
            def foo():
                # By the time this lines run, the database should have been reset so ex_table and qy_model should
                # have already a value
                assert qy_model.call_count == len(tables)

            foo()
            assert qy_model.call_count == len(tables)

            qy_model.reset_mock()

            # (2)
            @test_utils.reset_database(tear='down', db_models=tables)
            def bar():
                # By the time this lines run, the database should have been reset so ex_table and qy_model should
                # have already a value
                assert qy_model.call_count == 0

            bar()
            assert qy_model.call_count == len(tables)

            qy_model.reset_mock()

            # (3)
            @test_utils.reset_database(tear='up_down', db_models=tables)
            def foo_bar():
                # By the time this lines run, the database should have been reset so ex_table and qy_model should
                # have already a value
                assert qy_model.call_count == len(tables)

            foo_bar()
            assert qy_model.call_count == 2 * len(tables)


def test_fetch_setting_data_table(settings):
    table, *_ = settings

    # a) table should be a tuple
    assert table == (8, 8, 'GAME-START', 'GAME-END')


def test_fetch_setting_data_knights(settings):
    '''Ensure knights are dicts and the position is a tuple of two integers
    '''
    table, knights, *_ = settings

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
    *_, items = settings

    # --> Axe and MagicStaff items should be in
    assert all(item in items for item in ('A', 'M'))
    position = items['A']['position']
    # --> position is a tuple of two integers
    assert all(condition for condition in (len(position) == 2,
                                           isinstance(position, tuple),
                                           all(isinstance(x, int) for x in position)))


def test_get_game_settings(settings):
    '''a tuple with table, knights and dicts should be returned from any file settings
    '''
    table, knights, items = settings
    assert isinstance(table, tuple)
    assert isinstance(knights, dict)
    assert isinstance(items, dict)
