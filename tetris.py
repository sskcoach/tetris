# tetris.py

import os
import time
import random
import sys
import tty
import termios
import select
from itertools import zip_longest
from enum import Enum

# --- 게임 상태 정의 ---
class GameState(Enum):
    SPLASH = 1
    TITLE = 2
    GAME = 3
    NEXT_STAGE = 4
    GAME_OVER = 5

TETROMINOS = {
    'I': [['  ', '[]', '  ', '  '], ['  ', '[]', '  ', '  '], ['  ', '[]', '  ', '  '], ['  ', '[]', '  ', '  ']],
    'O': [['[]', '[]'], ['[]', '[]']],
    'T': [['  ', '[]', '  '], ['[]', '[]', '[]'], ['  ', '  ', '  ']],
    'J': [['  ', '[]', '  '], ['  ', '[]', '  '], ['[]', '[]', '  ']],
    'L': [['  ', '[]', '  '], ['  ', '[]', '  '], ['  ', '[]', '[]']],
    'S': [['  ', '[]', '[]'], ['[]', '[]', '  '], ['  ', '  ', '  ']],
    'Z': [['[]', '[]', '  '], ['  ', '[]', '[]'], ['  ', '  ', '  ']]
}

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
LEVEL_UP_LINES = 10

# --- 유틸리티 및 헬퍼 함수 ---

def rotate_clockwise(block):
    return [list(row[::-1]) for row in zip(*block)]

def create_empty_board(width, height):
    return [[' .' for _ in range(width)] for _ in range(height)]

def format_board(board):
    lines = ["◀" + "".join(row) + "▶" for row in board]
    lines.append("=" * (BOARD_WIDTH * 2 + 2))
    lines.append("\/" * ((BOARD_WIDTH * 2 + 2) // 2))
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

def draw_text_screen(title, subtitle):
    # This function is used to draw simple text screens like splash, title, game over
    print(f"\x1b[H\x1b[2J", end="") # 화면 지우기
    print("\n\n\n\n")
    print("="*30)
    print(f"{title:^30}")
    print("="*30)
    print("\n\n")
    print(f"{subtitle:^30}")
    print("\n\n")
    sys.stdout.flush()

# --- 각 SCENE 별 함수 ---

def run_splash_screen():
    draw_text_screen("TETRIS", "Made by Gemini")
    time.sleep(2)
    return GameState.TITLE

def run_title_screen(nbi):
    draw_text_screen("T E T R I S", "시작하려면 Enter를 누르세요")
    while True:
        char = nbi.get_char()
        if char == '\r' or char == '\n': # Enter key
            return GameState.GAME
        time.sleep(0.1)

def run_next_stage_screen(level):
    draw_text_screen(f"LEVEL {level-1} CLEAR!", f"잠시 후 LEVEL {level}을(를) 시작합니다.")
    time.sleep(3)
    return GameState.GAME

def run_game_over_screen(nbi, score):
    draw_text_screen("GAME OVER", f"최종 점수: {score}")
    print(f"{'다시 시작: Enter / 종료: Q':^30}")
    while True:
        char = nbi.get_char()
        if char == '\r' or char == '\n':
            return GameState.TITLE
        elif char == 'q':
            return None # Exit game
        time.sleep(0.1)

def run_game(nbi, level, score, total_lines_cleared):
    board = create_empty_board(BOARD_WIDTH, BOARD_HEIGHT)
    block_keys = list(TETROMINOS.keys())
    block_queue = []
    replenish_queue(block_queue, block_keys)
    replenish_queue(block_queue, block_keys)

    current_block_key = block_queue.pop(0)
    current_block_shape = TETROMINOS[current_block_key]
    block_position = [3, 0]
    
    gravity_timer = 0
    gravity_speed = max(1, 5 - level) # 레벨에 따라 속도 증가

    def handle_block_landing_in_game(board, shape, pos, queue, keys):
        board = place_block(board, shape, pos)
        board, lines_cleared = clear_lines(board)
        
        if len(queue) < 4:
            replenish_queue(queue, keys)
        
        next_key = queue.pop(0)
        new_shape = TETROMINOS[next_key]
        new_pos = [3, 0]
        
        is_game_over = check_collision(board, new_shape, new_pos)
        return board, new_shape, new_pos, is_game_over, queue, lines_cleared

    while True:
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
            board, current_block_shape, block_position, game_over, block_queue, lines_cleared = handle_block_landing_in_game(board, current_block_shape, block_position, block_queue, block_keys)
            if game_over: return GameState.GAME_OVER, score, total_lines_cleared
            total_lines_cleared += lines_cleared
            score += lines_cleared * 100 * level
            gravity_timer = 0
        elif char == 'q':
            return GameState.TITLE, score, total_lines_cleared

        if gravity_timer >= gravity_speed:
            gravity_timer = 0
            block_position[1] += 1
            if check_collision(board, current_block_shape, block_position):
                block_position[1] -= 1
                board, current_block_shape, block_position, game_over, block_queue, lines_cleared = handle_block_landing_in_game(board, current_block_shape, block_position, block_queue, block_keys)
                if game_over: return GameState.GAME_OVER, score, total_lines_cleared
                total_lines_cleared += lines_cleared
                score += lines_cleared * 100 * level

        if total_lines_cleared >= level * LEVEL_UP_LINES:
            return GameState.NEXT_STAGE, score, total_lines_cleared
        
        # --- 렌더링 ---
        temp_board = [row[:] for row in board]
        temp_board = place_block(temp_board, current_block_shape, block_position)
        
        board_lines = format_board(temp_board)
        preview_keys = block_queue[:3]
        preview_lines = format_preview(preview_keys)

        screen_buffer = [f"--- LEVEL: {level} | SCORE: {score} ---"]
        for board_line, preview_line in zip_longest(board_lines, preview_lines, fillvalue=""):
            screen_buffer.append(f"{board_line}  {preview_line}")
        screen_buffer.append(f"\n조작: a, d, w, s, 스페이스바 | 종료: q")
        full_screen_string = "\n".join(screen_buffer)

        print(f"\x1b[H\x1b[2J{full_screen_string}", end="")
        sys.stdout.flush()
        
        time.sleep(0.1)

# --- 메인 상태 관리 루프 ---
if __name__ == "__main__":
    current_state = GameState.SPLASH
    level = 1
    score = 0
    total_lines = 0

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        with NonBlockingInput() as nbi:
            while current_state is not None:
                if current_state == GameState.SPLASH:
                    current_state = run_splash_screen()
                elif current_state == GameState.TITLE:
                    current_state = run_title_screen(nbi)
                    level, score, total_lines = 1, 0, 0
                elif current_state == GameState.GAME:
                    next_state, score, total_lines = run_game(nbi, level, score, total_lines)
                    current_state = next_state
                elif current_state == GameState.NEXT_STAGE:
                    level += 1
                    current_state = run_next_stage_screen(level)
                elif current_state == GameState.GAME_OVER:
                    current_state = run_game_over_screen(nbi, score)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

    print("게임을 종료합니다.")