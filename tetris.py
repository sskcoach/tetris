# tetris.py

import os
import time
import random
import sys
import tty
import termios
import select
from itertools import zip_longest

TETROMINOS = {
    'I': [['  ', '[]', '  ', '  '],
          ['  ', '[]', '  ', '  '],
          ['  ', '[]', '  ', '  '],
          ['  ', '[]', '  ', '  ']],
    'O': [['[]', '[]'],
          ['[]', '[]']],
    'T': [['  ', '[]', '  '],
          ['[]', '[]', '[]'],
          ['  ', '  ', '  ']],
    'J': [['  ', '[]', '  '],
          ['  ', '[]', '  '],
          ['[]', '[]', '  ']],
    'L': [['  ', '[]', '  '],
          ['  ', '[]', '  '],
          ['  ', '[]', '[]']],
    'S': [['  ', '[]', '[]'],
          ['[]', '[]', '  '],
          ['  ', '  ', '  ']],
    'Z': [['[]', '[]', '  '],
          ['  ', '[]', '[]'],
          ['  ', '  ', '  ']]
}

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

def rotate_clockwise(block):
    return [list(row[::-1]) for row in zip(*block)]

def create_empty_board(width, height):
    return [[' .' for _ in range(width)] for _ in range(height)]

def format_board(board):
    lines = ["<|" + "".join(row) + "|>") for row in board]
    lines.append("=" * (BOARD_WIDTH * 2 + 4))
    lines.append("\/" * ((BOARD_WIDTH * 2 + 4) // 2))
    return lines

def format_preview(preview_keys):
    lines = ["  다음 블록"]
    lines.append(" " + "-"*10)
    if not preview_keys:
        return lines
    for key in preview_keys:
        shape = TETROMINOS[key]
        canvas = [['  ' for _ in range(4)] for _ in range(4)]
        shape_h, shape_w = len(shape), len(shape[0])
        start_y, start_x = (4 - shape_h) // 2, (4 - shape_w) // 2
        for r in range(shape_h):
            for c in range(shape_w):
                if shape[r][c] == '[]':
                    canvas[start_y + r][start_x + c] = '[]'
        for row in canvas:
            lines.append("  " + "".join(row))
        lines.append(" " + "-"*10)
    return lines

def replenish_queue(queue, keys):
    new_bag = list(keys)
    random.shuffle(new_bag)
    queue.extend(new_bag)

class NonBlockingInput:
    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
    def get_char(self):
        last_char = None
        while select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            last_char = sys.stdin.read(1)
        return last_char

def place_block(board, block_shape, position):
    pos_x, pos_y = position
    for r, row_data in enumerate(block_shape):
        for c, cell_data in enumerate(row_data):
            if cell_data == '[]':
                if 0 <= pos_y + r < len(board) and 0 <= pos_x + c < len(board[0]):
                    board[pos_y + r][pos_x + c] = '[]'
    return board

def check_collision(board, block_shape, position):
    pos_x, pos_y = position
    for r, row_data in enumerate(block_shape):
        for c, cell_data in enumerate(row_data):
            if cell_data == '[]':
                if not (0 <= pos_x + c < BOARD_WIDTH): return True
                if not (pos_y + r < BOARD_HEIGHT): return True
                if 0 <= pos_y + r < BOARD_HEIGHT and board[pos_y + r][pos_x + c] == '[]': return True
    return False

def clear_lines(board):
    new_board = [row for row in board if not all(cell == '[]' for cell in row)]
    lines_cleared = BOARD_HEIGHT - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [' .' for _ in range(BOARD_WIDTH)])
    return new_board, lines_cleared

def handle_block_landing(board, block_shape, position, block_queue, block_keys):
    board = place_block(board, block_shape, position)
    board, _ = clear_lines(board)
    if len(block_queue) < 4:
        replenish_queue(block_queue, block_keys)
    next_block_key = block_queue.pop(0)
    new_shape = TETROMINOS[next_block_key]
    new_position = [3, 0]
    game_over = check_collision(board, new_shape, new_position)
    return board, new_shape, new_position, game_over, block_queue

if __name__ == "__main__":
    with NonBlockingInput() as nbi:
        board = create_empty_board(BOARD_WIDTH, BOARD_HEIGHT)
        block_keys = list(TETROMINOS.keys())
        block_queue = []
        replenish_queue(block_queue, block_keys)
        replenish_queue(block_queue, block_keys)

        current_block_key = block_queue.pop(0)
        current_block_shape = TETROMINOS[current_block_key]
        block_position = [3, 0]
        game_over = False
        gravity_timer = 0
        gravity_speed = 5

        while not game_over:
            gravity_timer += 1
            char = nbi.get_char()

            if char == 'a':
                block_position[0] -= 1
                if check_collision(board, current_block_shape, block_position): block_position[0] += 1
            elif char == 'd':
                block_position[0] += 1
                if check_collision(board, current_block_shape, block_position): block_position[0] -= 1
            elif char == 'w':
                rotated = rotate_clockwise(current_block_shape)
                if not check_collision(board, rotated, block_position): current_block_shape = rotated
            elif char == 's':
                block_position[1] += 1
                if check_collision(board, current_block_shape, block_position): block_position[1] -= 1
            elif char == ' ':
                while not check_collision(board, current_block_shape, block_position):
                    block_position[1] += 1
                block_position[1] -= 1
                board, current_block_shape, block_position, game_over, block_queue = handle_block_landing(board, current_block_shape, block_position, block_queue, block_keys)
                gravity_timer = 0
            elif char == 'q':
                game_over = True

            if gravity_timer >= gravity_speed:
                gravity_timer = 0
                block_position[1] += 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[1] -= 1
                    board, current_block_shape, block_position, game_over, block_queue = handle_block_landing(board, current_block_shape, block_position, block_queue, block_keys)

            if not game_over:
                temp_board = [row[:] for row in board]
                temp_board = place_block(temp_board, current_block_shape, block_position)
                
                board_lines = format_board(temp_board)
                preview_keys = block_queue[:3]
                preview_lines = format_preview(preview_keys)

                os.system('cls' if os.name == 'nt' else 'clear')
                print("--- 테트리스 게임 ---")
                for board_line, preview_line in zip_longest(board_lines, preview_lines, fillvalue=""):
                    print(f"{board_line}  {preview_line}")
                print("\n조작: a(왼쪽), d(오른쪽), w(회전), s(아래로), 스페이스바(하드 드롭), q(종료)")
            
            time.sleep(0.1)

    print("--- GAME OVER ---")
    final_board_lines = format_board(board)
    for line in final_board_lines:
        print(line)