# tetris.py

# tetris.py

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

def rotate_clockwise(block):
    """
    주어진 블록을 시계 방향으로 90도 회전합니다.
    """
    return [list(row[::-1]) for row in zip(*block)]


def print_block(block):
    """
    주어진 블록 모양을 터미널에 출력합니다.
    """
    for row in block:
        print("".join(row))

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

def create_empty_board(width, height):
    """
    지정된 너비와 높이의 빈 테트리스 보드를 생성합니다.
    빈 공간은 ' .'으로 채워집니다.
    """
    board = [[' .' for _ in range(width)] for _ in range(height)]
    return board

def draw_board(board):
    """
    테트리스 보드를 터미널에 그립니다.
    양쪽 벽은 <| 와 |> 형태이고, 바닥은 ====== 와 \/\/\/ 형태입니다.
    """
    for row in board:
        print("<|" + "".join(row) + "|>")
    
    # 바닥 경계선
    print("=" * (BOARD_WIDTH * 2 + 4)) # 셀 너비가 2이므로 *2, 벽 너비 +4
    print("\\/" * ((BOARD_WIDTH * 2 + 4) // 2)) # \\/가 2칸이므로 전체 너비/2


import os
import time
import random
import sys
import tty
import termios
import select

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
    """
    주어진 위치에 블록을 보드에 배치합니다.
    """
    pos_x, pos_y = position
    for r, row_data in enumerate(block_shape):
        for c, cell_data in enumerate(row_data):
            if cell_data == '[]':
                # 보드 경계를 확인합니다.
                if 0 <= pos_y + r < len(board) and 0 <= pos_x + c < len(board[0]):
                    board[pos_y + r][pos_x + c] = '[]'
    return board # 수정된 보드를 반환합니다.

def check_collision(board, block_shape, position):
    """
    주어진 위치에서 블록이 보드 경계나 다른 블록과 충돌하는지 확인합니다.
    """
    pos_x, pos_y = position
    for r, row_data in enumerate(block_shape):
        for c, cell_data in enumerate(row_data):
            if cell_data == '[]':
                if not (0 <= pos_x + c < BOARD_WIDTH):
                    return True
                if not (pos_y + r < BOARD_HEIGHT):
                    return True
                if 0 <= pos_y + r < BOARD_HEIGHT and board[pos_y + r][pos_x + c] == '[]':
                    return True
    return False

def clear_lines(board):
    """
    가득 찬 줄을 지우고, 지운 만큼 위에 새로운 빈 줄을 추가합니다.
    """
    lines_cleared = 0
    new_board = []
    for row in board:
        if all(cell == '[]' for cell in row):
            lines_cleared += 1
        else:
            new_board.append(row)
    
    for _ in range(lines_cleared):
        new_board.insert(0, [' .' for _ in range(BOARD_WIDTH)])
        
    return new_board, lines_cleared

def handle_block_landing(board, block_shape, position, block_keys):
    """
    블록 착지 시의 로직(합치기, 줄 제거, 새 블록 생성)을 처리합니다.
    """
    board = place_block(board, block_shape, position)
    board, _ = clear_lines(board) # lines_cleared는 나중에 점수계산에 사용
    
    new_shape = TETROMINOS[random.choice(block_keys)]
    new_position = [3, 0]
    
    game_over = check_collision(board, new_shape, new_position)
    
    return board, new_shape, new_position, game_over

if __name__ == "__main__":
    with NonBlockingInput() as nbi:
        board = create_empty_board(BOARD_WIDTH, BOARD_HEIGHT)
        block_keys = list(TETROMINOS.keys())
        current_block_shape = TETROMINOS[random.choice(block_keys)]
        block_position = [3, 0]
        game_over = False
        
        gravity_timer = 0
        gravity_speed = 5

        while not game_over:
            gravity_timer += 1
            char = nbi.get_char()

            if char == 'a':
                block_position[0] -= 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[0] += 1
            
            elif char == 'd':
                block_position[0] += 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[0] -= 1

            elif char == 'w':
                rotated_block = rotate_clockwise(current_block_shape)
                if not check_collision(board, rotated_block, block_position):
                    current_block_shape = rotated_block

            elif char == 's':
                block_position[1] += 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[1] -= 1
            
            elif char == ' ': # 하드 드롭
                while not check_collision(board, current_block_shape, block_position):
                    block_position[1] += 1
                block_position[1] -= 1
                board, current_block_shape, block_position, game_over = handle_block_landing(board, current_block_shape, block_position, block_keys)
                gravity_timer = 0
            
            elif char == 'q':
                game_over = True

            if gravity_timer >= gravity_speed:
                gravity_timer = 0
                block_position[1] += 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[1] -= 1
                    board, current_block_shape, block_position, game_over = handle_block_landing(board, current_block_shape, block_position, block_keys)

            if not game_over:
                temp_board = [row[:] for row in board]
                temp_board = place_block(temp_board, current_block_shape, block_position)

                os.system('cls' if os.name == 'nt' else 'clear')
                print("--- 테트리스 게임 ---")
                draw_board(temp_board)
                print("조작: a(왼쪽), d(오른쪽), w(회전), s(아래로), 스페이스바(하드 드롭), q(종료)")
            
            time.sleep(0.1)

    print("--- GAME OVER ---")
    draw_board(board)


