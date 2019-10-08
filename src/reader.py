import yaml
from src.errors import InstructionError


class InstructionReader:

    def __init__(self, start, end):
        self.heading = start
        self.footer = end
        self.instructions = []

    def parse_lines(self, content):
        eof = False
        for offset, line in enumerate(content):
            # is is the first line of the file complaint
            if not offset:
                if self.heading != line:
                    raise InstructionError(f'Error at line {offset}: the heading of instructions file should be '
                                           f'{self.heading}. Instead {line}.')
            else:
                # Have we found the end of the file?
                if line == self.footer:
                    if eof:
                        raise InstructionError(f"Error at line {offset}: footer has already being found.")
                    eof = True
                # ... Otherwise fetch the instruction
                else:
                    instruction = line.split(':')
                    if len(instruction) != 2:
                        raise InstructionError(f"Error at line{offset}: Wrong format of instruction '{line}'")
                    self.instructions.append(instruction)

    def extract(self, filename):
        '''Read the content of a file and extract instructions
        '''
        with open(filename) as fh:
            self.parse_lines(line.strip('\r\n') for line in fh)

    def __len__(self):
        return len(self.instructions)

    def __getitem__(self, item):
        return self.instructions[item]

    def __iter__(self):
        return iter(self.instructions)


class SettingReader:

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