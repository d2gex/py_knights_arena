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
