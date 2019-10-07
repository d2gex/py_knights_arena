from src.cell_content import Knight, Item, KNIGHT_LIVE, KNIGHT_DEAD, KNIGHT_DROWNED, ITEM_USED


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.arena = [[None for self.columns in range(columns)] for self.rows in range(rows)]
        self.knights = None
        self.items = None

    def set_knights(self, knights):
        '''Create a dictionary of knights as Cell Content objects and place them on the arena
        '''
        self.knights = {nickname: Knight(data['name'],
                                         nickname,
                                         KNIGHT_LIVE,
                                         data['attack'],
                                         data['defence']) for nickname, data in knights.items()}
        for nickname, data in knights.items():
            x, y = data['position']
            self.arena[x][y] = [nickname]

    def set_items(self, items):
        '''Create a dictionary of items as Cell Content objects and place them on the arena
        '''
        self.items = {nickname: Item(data['name'],
                                     nickname,
                                     ITEM_USED,
                                     data['attack'],
                                     data['defence']) for nickname, data in items.items()}
        for nickname, data in items.items():
            x, y = data['position']
            self.arena[x][y] = [nickname]

    def __len__(self):
        return len(self.arena)

    def __getitem__(self, item):
        return self.arena[item]
