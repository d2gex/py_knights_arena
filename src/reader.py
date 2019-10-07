import yaml


class Reader:

    def __init__(self):
        self._instructions = None

    @property
    def instructions(self):
        return self._instructions

    @staticmethod
    def fetch_setting_data(settings):
        '''Given a settings dictionary creates a table tuple and two separate knights and items dictionary with
        data about them, respectively
        '''

        # create table tuple
        table = (settings['table']['rows'], settings['table']['columns'])

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

    def get_game_settings(self, filename):
        with open(filename) as fh:
            return self.fetch_setting_data(yaml.safe_load(fh))
