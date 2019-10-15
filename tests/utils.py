import functools
import yaml

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


def fetch_setting_data(settings):
    '''Given a settings dictionary creates a table tuple and two separate knights and items dictionary with
    data about them, respectively
    '''

    # create table tuple
    s_table = settings['table']
    table = (s_table['rows'], s_table['columns'], s_table['start'], s_table['end'])

    # create knights dictionary
    knights = {}
    for kn_dict in settings['knights']:
        nickname = kn_dict['nickname']
        knights[nickname] = {}
        del kn_dict['nickname']
        knights[nickname] = {key: value if key != 'position' else tuple(int(coord) for coord in value.split(','))
                             for key, value in kn_dict.items()}

    items = {}
    for item_dict in settings['items']:
        nickname = item_dict['nickname']
        items[nickname] = {}
        del item_dict['nickname']
        items[nickname] = {key: value if key != 'position' else tuple(int(coord) for coord in value.split(','))
                           for key, value in item_dict.items()}

    return table, knights, items


def get_game_settings(filename):
    with open(filename) as fh:
        return fetch_setting_data(yaml.safe_load(fh))
