from src.cell_content import Knight, Item

KNIGHT_LIVE = 0
KNIGHT_DROWNED = 1
KNIGHT_DEAD = 2
ITEM_USED = False


class Board:

    def __init__(self, rows, columns):
        self.arena = [[None for column in range(columns)] for row in range(rows)]
        self.knights = None
        self.items = None

    def set_knights(self, knights):
        '''Create a dictionary of knights as Cell Content objects and place them on the arena
        '''
        self.knights = {name: Knight(name,
                                     data['nickname'],
                                     KNIGHT_LIVE,
                                     data['attack'],
                                     data['defence']) for name, data in knights.items()}
        for name, data in knights.items():
            x, y = data['position']
            self.arena[x][y] = [name]

    def set_items(self, items):
        '''Create a dictionary of items as Cell Content objects and place them on the arena
        '''
        self.items = {name: Knight(name,
                                   data['nickname'],
                                   ITEM_USED,
                                   data['attack'],
                                   data['defence']) for name, data in items.items()}
        for name, data in items.items():
            x, y = data['position']
            self.arena[x][y] = [name]

    def __len__(self):
        return len(self.arena)

    def __getitem__(self, item):
        return self.arena[item]
