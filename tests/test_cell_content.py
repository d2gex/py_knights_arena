import pytest
from src.cell_content import Item
from tests.utils import ItemFactory, KnightFactory


@pytest.fixture(scope='module')
def items():
    return ItemFactory.all()


@pytest.fixture(scope='module')
def knights(items):
    axe, magic_staff, dagger, helmet = items
    kn1, kn2, kn3, kn4 = KnightFactory.all()
    kn1.item, kn2.item, kn3.item, kn4.item = axe, magic_staff, dagger, helmet
    return kn1, kn2, kn3, kn4


def test_item_power(items):
    axe, magic_staff, dagger, helmet = items
    # axe is por powerful than anything else
    assert all(axe > item for item in(magic_staff, dagger, helmet))

    # magi_staff is the second most powerful
    assert all(magic_staff > item for item in(dagger, helmet))

    # dagger is more powerful than helmet
    assert dagger > helmet

    # Those items that are the same are the same powerful
    assert axe >= Item('Axe', 'A', status=False, attack_score=2, defence_score=0)


class TestKnights:
    '''knights on attack:   (surprise + base + attack)
    a) kn1(axe) =>          (0.5 + 1 + 2) = 3.5
    b) kn2(magic_staff) =>  (0.5 + 1 + 1) = 2.5
    c) kn3(dagger) =>       (0.5 + 1 + 1) = 2.5
    d) kn4(helmet) =>       (0.5 + 1 + 0) = 1.5

    knights on defence: (base + defence)
    e) kn1(axe) =>          (1 + 0) = 1
    f) kn2(magic_staff) =>  (1 + 1) = 2
    g) kn3(dagger) =>       (1 + 0) = 1
    h) kn4(helmet) =>       (1 + 1) = 2
    '''

    def test_knight_with_axe_attack(self, knights):
        '''On attack knight with axe beats everybody
        '''
        kn1, kn2, kn3, kn4 = knights
        assert all(kn1.beat(knight) for knight in (kn2, kn3, kn4))

    def test_knight_with_axe_defence(self, knights):
        '''On defence knight with axe is beaten by everybody
        '''
        kn1, kn2, kn3, kn4 = knights
        assert all(knight.beat(kn1) for knight in (kn2, kn3, kn4))

    def test_knight_with_magic_staff_attack(self, knights):
        '''On attack knight with magic_staff beats everybody
        '''
        kn1, kn2, kn3, kn4 = knights
        assert all(kn2.beat(knight) for knight in (kn1, kn3, kn4))

    def test_knight_with_magic_staff_defence(self, knights):
        '''On defence knight with magic_staff is only beaten by those either with axe or dagger
        '''
        kn1, kn2, kn3, kn4 = knights
        assert not kn4.beat(kn2)
        assert all(knight.beat(kn2) for knight in (kn1, kn3))

    def test_knight_with_dagger_attack(self, knights):
        '''On attack knight with dagger beats everybody
        '''
        kn1, kn2, kn3, kn4 = knights
        assert all(kn3.beat(knight) for knight in (kn1, kn2, kn4))

    def test_knight_with_dagger_defence(self, knights):
        '''On defence knight with dagger is beaten by everybody
        '''
        kn1, kn2, kn3, kn4 = knights
        assert all(knight.beat(kn3) for knight in (kn1, kn2, kn4))

    def test_knight_with_helmet_attack(self, knights):
        '''On attack knight with helmet only beats axe and dagger
        '''
        kn1, kn2, kn3, kn4 = knights
        assert not kn4.beat(kn2)
        assert all(kn4.beat(knight) for knight in (kn1, kn3))

    def test_knight_with_helmet_defence(self, knights):
        '''On defence knight with helmet is beaten by everybody
        '''
        kn1, kn2, kn3, kn4 = knights
        assert all(knight.beat(kn4) for knight in (kn1, kn2, kn3))

    def test_pick_items(self):
        '''A knight will:
        a) pick an item if none
        b) ignore item if one already assigned
        c) pick the best item of various, including the one given following an order of [A,M,D,H]
        '''

        # a)
        red = KnightFactory.red()
        axe = ItemFactory.axe()
        assert not red.item
        red.pick_item(axe)
        assert red.item == axe

        # b)
        magic_staff = ItemFactory.magic_staff()
        red.pick_item(magic_staff)
        assert red.item == axe

        # c)
        red.item = None
        helmet = ItemFactory.helmet()
        red.pick_item(helmet)
        assert red.item == helmet
        red.pick_item([magic_staff, axe])
        assert red.item == axe

        # c.1
        # --> if the most powerful is the one held ignore the rest
        red.pick_item([magic_staff, helmet])
        assert red.item == axe

        # c.2
        dagger = ItemFactory.dagger()
        red.item = dagger
        red.pick_item([magic_staff, helmet])
        assert red.item == magic_staff
