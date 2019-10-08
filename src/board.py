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

    def move_and_drown(self, origin, knight_nk, item_nk):
        '''update the board when a knight move ends up in drowning.

        a) if a knight with no item drowns its position is updated to None and its status to DROWNED
        b) if in addition it has an item => leaves the item into the tile that was standing before drowning
        '''
        x, y = origin
        self.knights[knight_nk].status = KNIGHT_DROWNED
        self.expunge_cell(x, y, knight_nk)
        self.k_positions[knight_nk] = None
        if item_nk:
            self.update_cell(x, y, item_nk)
            self.items[item_nk] = x, y

    def move_to_empty_cell(self, origin, dest, knight_nk, item_nk):
        '''Update the board when a knight moves into an empty cell.

        a) if knight has not item the position of if is updated.
        b) if in addition it has an item the position of the item is too updated
        '''

        o_x, o_y = origin
        d_x, d_y = dest
        self.expunge_cell(o_x, o_y, knight_nk)
        self.update_cell(d_x, d_y, knight_nk)
        self.k_positions[knight_nk] = d_x, d_y
        if item_nk:
            self.i_positions[item_nk] = d_x, d_y

    def move_to_single_item_cell(self, origin, dest, knight_nk, item_nk, new_item_nk):
        '''Update the board when a knight moves into a cell with an item.

        a) If the knight has not item then picks it, removes it from the cell and update the item position.
        b) Otherwise ignores it.
        '''

        d_x, d_y = dest
        self.move_to_empty_cell(origin, dest, knight_nk, item_nk)
        # If not item => pick it up
        if not item_nk:
            self.knights[knight_nk].pick_item(new_item_nk)
            self.i_positions[new_item_nk] = d_x, d_y
            self.expunge_cell(d_x, d_y, new_item_nk)

    def move(self, knight, direction):
        '''
        '''
        to_x, to_y = self.k_positions[knight]
        from_x, from_y = to_x, to_y
        kn = self.knights[knight]
        knight_nk = kn.nickname
        item_nk = kn.item.nickname if kn.item else None
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
            self.move_and_drown((from_x, from_y), knight_nk, item_nk)
        else:
            try:
                cell = list(self.arena[to_x][to_y])
            except TypeError:
                cell = None
            # did knight move to an empty cell?
            if not cell:
                self.move_to_empty_cell((from_x, from_y), (to_x, to_y), knight_nk, item_nk)
            elif len(cell) == 1:
                # is it a cell with one single item
                if cell[0] in self.items:
                    new_item_nk = cell[0]
                    self.move_to_single_item_cell((from_x, from_y), (to_x, to_y), knight_nk, item_nk, new_item_nk)
                # is it a knight => time to fight
                else:
                    pass

    def __len__(self):
        return len(self.arena)

    def __getitem__(self, item):
        return self.arena[item]

    def __str__(self):
        return "\n|" + \
               "\n|".join(f"{'|'.join(str(column).center(10, ' ') if column is not None else ' '.center(10, ' ') for column in row)}|" for row in self.arena)
