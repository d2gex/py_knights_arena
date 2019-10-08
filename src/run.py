import sys

from os.path import join
from src.reader import InstructionReader, SettingReader
from src.board import Board


def to_file(content, path):
    with open(path, 'w') as fh:
        fh.write(content)


def run(s_filename, i_filename, data_folder):
    s_reader = SettingReader()
    arena, knights, items = s_reader.get_game_settings(s_filename)
    rows, columns, start, end = arena
    instructions = InstructionReader(start, end)
    instructions.extract(i_filename)
    board = Board(rows, columns)
    board.set_knights(knights)
    board.set_items(items)
    to_file(str(board), join(data_folder, 'board_map_before.txt'))
    to_file(board.to_json(), join(data_folder, 'board_json_before.txt'))
    for instruction in instructions:
        knight, direction = instruction
        board.move(knight, direction)
    to_file(str(board), join(data_folder, 'board_map_after.txt'))
    to_file(board.to_json(), join(data_folder, 'board_json_after.txt'))


if __name__ == "__main__":
    setting_filename = sys.argv[1]
    instruction_filename = sys.argv[2]
    debug_folder = sys.argv[3]

    run(setting_filename, instruction_filename, debug_folder)
