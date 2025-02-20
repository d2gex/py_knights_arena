KNIGHT_LIVE = 'LIVE'
KNIGHT_DROWNED = 'DROWNED'
KNIGHT_DEAD = 'DEAD'
ITEM_USED = False


class CellContent:

    def __init__(self, name, nickname, status, attack_score, defence_score):
        self.name = name
        self.nickname = nickname
        self._attack_score = attack_score
        self._defence_score = defence_score
        self._status = status

    @property
    def attack_score(self):
        return self._attack_score

    @attack_score.setter
    def attack_score(self, new_score):
        self._attack_score = new_score

    @property
    def defence_score(self):
        return self._defence_score

    @defence_score.setter
    def defence_score(self, new_score):
        self._defence_score = new_score

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status):
        self._status = new_status

    def __str__(self):
        return self.nickname


class Item(CellContent):

    def __gt__(self, other):
        '''An item is more powerful than another one if this has either more attacking power or having the same
        it has more defence power.
        '''
        if self.attack_score > other.attack_score:
            return True
        if self.attack_score < other.attack_score:
            return False
        return self.defence_score > other.defence_score

    def __ge__(self, other):
        if self.attack_score + self.defence_score - other.attack_score + other.defence_score == 0:
            return True
        return self.__gt__(other)


class Knight(CellContent):

    def __init__(self, *args, surprise=0.5):
        super().__init__(*args)
        self.surprise = surprise
        self._item = None

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, new_item):
        self._item = new_item

    def pick_item(self, items):
        '''A knight will pick the most powerful item available when given a few of them based on
        '''
        if isinstance(items, Item):
            if not self.item:
                self._item = items
        else:
            self._item = sorted(items + [self.item] if self.item else items, reverse=True)[0]

    def beat(self, knight):
        '''At knight beats another knight if its attacking power is bigger than its rival defensive one
        '''
        return (self.surprise + self.attack_score + self.item.attack_score) > \
               (knight.defence_score + knight.item.defence_score)

    def __str__(self):
        '''Return its nickname in uppercase if the knight is still alive or in lowercase otherwise
        '''
        return self.nickname if self.status == KNIGHT_LIVE else self.nickname.lower()
