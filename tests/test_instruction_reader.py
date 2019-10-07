import pytest

from os.path import join
from src.instruction_reader import InstructionReader
from src.errors import InstructionError
from tests import utils as test_utils

HEADING = 'GAME-START'
FOOTER = 'GAME-END'


@pytest.fixture(autouse=True)
def i_reader():
    ins = InstructionReader(HEADING, FOOTER)
    return ins


def test_wrong_start(i_reader):
    '''Check instruction file provide the expected heading in line 0
    '''
    lines = ['unexpected start']
    with pytest.raises(InstructionError) as ex:
        i_reader.parse_lines(lines)
    assert all(x in str(ex.value) for x in ('0', 'heading'))


def test_wrong_instruction(i_reader):
    '''Check instruction has the right format
    '''
    lines = [HEADING, 'wrong instruction']
    with pytest.raises(InstructionError) as ex:
        i_reader.parse_lines(lines)
    assert all(x in str(ex.value) for x in ('1', 'Wrong format'))
    assert not i_reader.instructions

    # The second heading will be treated as an instruction and reported as error
    lines = [HEADING, HEADING]
    with pytest.raises(InstructionError) as ex:
        i_reader.parse_lines(lines)
    assert all(x in str(ex.value) for x in ('1', 'Wrong format'))
    assert not i_reader.instructions


def test_duplicate_footer(i_reader):
    '''Footer can only appear once
    '''
    lines = [HEADING, 'knight:move', FOOTER, FOOTER]
    with pytest.raises(InstructionError) as ex:
        i_reader.parse_lines(lines)
    assert all(x in str(ex.value) for x in ('3', 'footer has already being found'))


def test_correct_line(i_reader):
    assert not i_reader.instructions
    instruction = 'knight:move'
    lines = [HEADING, instruction, FOOTER]
    i_reader.parse_lines(lines)
    assert len(i_reader.instructions)
    assert i_reader[0] == instruction.split(':')


def test_extract(i_reader):
    i_reader.extract(join(test_utils.TEST, 'stubs', 'instructions.txt'))
    assert len(i_reader) == 3
    assert i_reader[0] == ['R', 'N']
    assert i_reader[1] == ['G', 'S']
    assert i_reader[2] == ['Y', 'E']