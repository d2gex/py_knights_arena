from os.path import join
from pathlib import Path

path = Path(__file__).resolve()
ROOT = path.parents[1]
TEST = join(ROOT, 'tests')


class ItemFactory:

    @classmethod
    def axe(cls):
        return Item('Axe', 'A', status=False, attack_score=2, defence_score=0)

    @classmethod
    def magic_staff(cls):
        return Item('MagicStaff', 'M', status=False, attack_score=1, defence_score=1)

    @classmethod
    def dagger(cls):
        return Item('Dagger', 'D', status=False, attack_score=1, defence_score=0)

    @classmethod
    def helmet(cls):
        return Item('Helmet', 'H', status=False, attack_score=0, defence_score=1)

    @classmethod
    def all(cls):
        return cls.axe(), cls.magic_staff(), cls.dagger(), cls.helmet()


class KnightFactory:

    @classmethod
    def red(cls):
        return Knight('RED', 'R', 'LIVE', 1, 1)

    @classmethod
    def green(cls):
        return Knight('GREEN', 'G', 'LIVE', 1, 1)

    @classmethod
    def blue(cls):
        return Knight('BLUE', 'B', 'LIVE', 1, 1)

    @classmethod
    def yellow(cls):
        return Knight('YELLOW', 'Y', 'LIVE', 1, 1)

    @classmethod
    def all(cls):
        return cls.red(), cls.green(), cls.blue(), cls.yellow()