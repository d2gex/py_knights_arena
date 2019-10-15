import functools

from os.path import join
from pathlib import Path
from src import models
from src.app import db

path = Path(__file__).resolve()
ROOT = path.parents[1]
TEST = join(ROOT, 'tests')


all_models = [models.Settings, models.Moves, models.Round, models.Player, models.Items, models.PlayerStatus]


def reset_database(tear='up', db_models=None):
    ''' Reset the database before, after or before and after the method being decorated is executed.
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _db_models = all_models if not db_models else db_models

            def run_queries():
                for db_model in _db_models:
                    db.session.query(db_model).delete()

            if tear in ('up', 'up_down'):
                run_queries()
                db.session.commit()
            ret = func(*args, **kwargs)
            if tear in ('down', 'up_down'):
                run_queries()
                db.session.commit()
            return ret
        return wrapper
    return decorator
