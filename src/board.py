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

    def move_to_cell_with_items_only(self, origin, dest, knight_nk, item_nk):
        '''Update the board when a knight moves into a cell with items only as follows:

        a) If knight has no item pick one
        b) if knight has item and there are two or more items pick the best item of them all
        c) Otherwise the knight keeps the item it had before entering in this cell

        For a) to c) both the item and the knight position is updated. For case b) the cell is updated with the knight's
        item if this picks one of the items in the cell.
        '''

        o_x, o_y = origin
        d_x, d_y = dest
        items = [self.items[x] for x in self.arena[d_x][d_y]]
        knight = self.knights[knight_nk]

        # Do we need to update the knight item?
        if not item_nk or len(items) > 1:

            if not item_nk:
                knight.pick_item(items)
                self.expunge_cell(d_x, d_y, knight.item.nickname)
            else:
                old_item_nk = knight.item.nickname
                knight.pick_item(items)
                # Update the cell with the new item if the knight picked up a new one
                self.expunge_cell(d_x, d_y, old_item_nk)
                self.update_cell(d_x, d_y, knight.item.nickname)

        # Update origin and destination cells
        self.expunge_cell(o_x, o_y, knight_nk)
        self.update_cell(d_x, d_y, knight_nk)
        # Update knight and item position
        self.k_positions[knight_nk] = d_x, d_y
        self.i_positions[knight.item.nickname] = d_x, d_y

    def move_to_cell_with_knights(self, origin, dest, knight_nk):
        '''Update the board when a knight moves into a cell with another knight. The use cases are as follow

        a) if the attacker has no item => white flag and avoid fight
        b) if there is no defender with item -> white flag and avoid fight
        c) if attacker has an item and there is a defender with item => fight so that:
            c.1) the loser leaves the item on the tile and update its defence and attack scores to 0

        The attacker always update its position
        '''
        o_x, o_y = origin
        d_x, d_y = dest

        # move attacker to new cell
        self.expunge_cell(o_x, o_y, knight_nk)
        self.update_cell(d_x, d_y, knight_nk)
        self.k_positions[knight_nk] = d_x, d_y
        a_knight = self.knights[knight_nk]

        # does the attacker have an item?
        if a_knight.item:

            # update the position of the attacker's item
            self.i_positions[a_knight.item.nickname] = d_x, d_y

            # Find a defender with an item
            defender_nk = None
            for nickname in self.arena[d_x][d_y] - {a_knight.nickname}:
                try:
                    knight = self.knights[nickname]
                except KeyError:
                    pass
                else:
                    if knight.item:
                        defender_nk = knight.nickname
                        break

            # if defender found => fight
            if defender_nk:
                d_knight = self.knights[defender_nk]
                loser = d_knight if a_knight.beat(d_knight) else a_knight
                loser.item = None
                loser.attack_score = 0
                loser.defence_score = 0
                loser.status = KNIGHT_DEAD

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
            origin = (from_x, from_y)
            dest = (to_x, to_y)
            try:
                cell = list(self.arena[to_x][to_y])
            except TypeError:
                cell = None
            # did knight move to an empty cell?
            if not cell:
                self.move_to_empty_cell(origin, dest, knight_nk, item_nk)
            # did it to a cell with items only?
            elif all(content in self.items for content in cell):
                self.move_to_cell_with_items_only(origin, dest, knight_nk, item_nk)
            # ... or are there both knights and items
            else:
                self.move_to_cell_with_knights(origin, dest, knight_nk)

    def __len__(self):
        return len(self.arena)

    def __getitem__(self, item):
        return self.arena[item]

    def __str__(self):
        return "\n|" + \
               "\n|".join(f"{'|'.join(str(column).center(10, ' ') if column is not None else ' '.center(10, ' ') for column in row)}|" for row in self.arena)
