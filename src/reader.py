import yaml


class Reader:

    def __init__(self):
        self._settings = None
        self._instructions = None

    @property
    def settings(self):
        return self._settings

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
            name = kn_dict['name']
            knights[name] = {}
            del kn_dict['name']
            knights[name] = {key: value if key != 'position' else tuple(int(coord) for coord in value.split(','))
                             for key, value in kn_dict.items()}

        items = {}
        for item_dict in settings['items']:
            name = item_dict['name']
            items[name] = {}
            del item_dict['name']
            items[name] = {key: value if key != 'position' else tuple(int(coord) for coord in value.split(','))
                           for key, value in item_dict.items()}

        return table, knights, items

    def read_settings(self, filename):
        with open(filename) as fh:
            self._settings = self.fetch_setting_data(yaml.safe_load(fh))
