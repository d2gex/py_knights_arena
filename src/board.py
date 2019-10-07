from src.cell_content import Knight, Item, KNIGHT_LIVE, KNIGHT_DEAD, KNIGHT_DROWNED, ITEM_USED


class Board:

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.arena = [[None for y in range(self.columns)] for x in range(self.rows)]
        self.knights = None
        self.items = None
        self.k_positions = {}
        self.i_positions = {}

    def set_knights(self, knights):
        '''Create a dictionary of knights as Cell Content objects and place them on the arena, updating the dictionary of
        positions for knights
        '''
        self.knights = {nickname: Knight(data['name'],
                                         nickname,
                                         KNIGHT_LIVE,
                                         data['attack'],
                                         data['defence']) for nickname, data in knights.items()}
        for nickname, data in knights.items():
            x, y = data['position']
            self.arena[x][y] = {nickname}
            self.k_positions[nickname] = data['position']

    def set_items(self, items):
        '''Create a dictionary of items as Cell Content objects and place them on the arena, updating the dictionary of
        positions for items
        '''
        self.items = {nickname: Item(data['name'],
                                     nickname,
                                     ITEM_USED,
                                     data['attack'],
                                     data['defence']) for nickname, data in items.items()}
        for nickname, data in items.items():
            x, y = data['position']
            self.arena[x][y] = {nickname}
            self.i_positions[nickname] = data['position']

    def remove_cell_item(self, x, y, item):
        cell = self.arena[x][y]
        cell.remove(item)
        if not cell:
            self.arena[x][y] = None

    def move(self, knight, direction):
        x, y = self.k_positions[knight]
        a_x, a_y = x, y
        kn = self.knights[knight]
        if direction == 'S':
            x += 1
        elif direction == 'N':
            x -= 1
        elif direction == 'E':
            y += 1
        else:
            y -= 1

        # did the knight fatally step out of the arena? => drowned
        if any((x < 0, y < 0, x >= self.rows, y >= self.columns)):
            kn.status = KNIGHT_DROWNED
            self.remove_cell_item(a_x, a_y, kn.nickname)
            self.k_positions[kn.nickname] = None
        else:
            pass

    def __len__(self):
        return len(self.arena)

    def __getitem__(self, item):
        return self.arena[item]

    def __str__(self):
        return "\n|" + \
               "\n|".join(f"{'|'.join(str(column).center(9, ' ') if column is not None else ' '.center(9, ' ') for column in row)}|" for row in self.arena)
