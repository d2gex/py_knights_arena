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

    def expunge_cell(self, x, y, content):
        '''Remove the given content from a cell and makes it None if it holds no longer elements
        '''
        cell = self.arena[x][y]
        cell.remove(content)
        if not cell:
            self.arena[x][y] = None

    def update_cell(self, x, y, content):
        '''Update a cell by adding the given content to it. If cell was None a new set with the given element
        is created
        '''
        cell = self.arena[x][y]
        if cell:
            cell.add(content)
        else:
            self.arena[x][y] = {content}

    def move_and_drown(self, origin, knight, item):
        '''update the board when a knight move ends up in drowning. If the knight has got an item it leaves it
        on the tile previous to sinking
        '''
        x, y = origin
        knight.status = KNIGHT_DROWNED
        self.expunge_cell(x, y, knight.nickname)
        self.k_positions[knight.nickname] = None
        if item:
            self.update_cell(x, y, item)
            self.items[item.nickname] = x, y

    def move_to_empty_cell(self, origin, dest, knight, item):
        '''Update the board when a knight moves into an empty cell. If the knight has got an item, the position of
        the item needs to be updated too.
        '''

        o_x, o_y = origin
        d_x, d_y = dest
        self.expunge_cell(o_x, o_y, knight.nickname)
        self.update_cell(d_x, d_y, knight.nickname)
        self.k_positions[knight.nickname] = d_x, d_y
        if item:
            self.i_positions[item.nickname] = d_x, d_y

    def move(self, knight, direction):
        '''
        '''
        to_x, to_y = self.k_positions[knight]
        from_x, from_y = to_x, to_y
        kn = self.knights[knight]
        item = kn.item if kn.item else None
        if direction == 'S':
            to_x += 1
        elif direction == 'N':
            to_x -= 1
        elif direction == 'E':
            to_y += 1
        else:
            to_y -= 1

        # did knight drowned?
        if any((to_x < 0, to_y < 0, to_x >= self.rows, to_y >= self.columns)):
            self.move_and_drown((from_x, from_y), kn, item)
        else:
            # did knight move to an empty cell?
            if not self.arena[to_x][to_y]:
                self.move_to_empty_cell((from_x, from_y), (to_x, to_y), kn, item)

    def __len__(self):
        return len(self.arena)

    def __getitem__(self, item):
        return self.arena[item]

    def __str__(self):
        return "\n|" + \
               "\n|".join(f"{'|'.join(str(column).center(9, ' ') if column is not None else ' '.center(9, ' ') for column in row)}|" for row in self.arena)
