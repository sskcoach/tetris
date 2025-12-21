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
                # 벽 충돌 확인
                if not (0 <= pos_x + c < BOARD_WIDTH):
                    return True
                # 바닥 충돌 확인
                if not (pos_y + r < BOARD_HEIGHT):
                    return True
                # 다른 블록과 충돌 확인 (y+r이 보드 안에 있을 때만)
                if 0 <= pos_y + r < BOARD_HEIGHT and board[pos_y + r][pos_x + c] == '[]':
                    return True
    return False

if __name__ == "__main__":
    with NonBlockingInput() as nbi:
        board = create_empty_board(BOARD_WIDTH, BOARD_HEIGHT)
        block_keys = list(TETROMINOS.keys())
        current_block_shape = TETROMINOS[random.choice(block_keys)]
        block_position = [3, 0]
        game_over = False
        
        gravity_timer = 0
        gravity_speed = 5 # 5 * 0.1초 = 0.5초마다 한 칸씩 하강
        
        while not game_over:
            gravity_timer += 1
            
            # --- 입력 처리 ---
            char = nbi.get_char()
            
            if char == 'a': # 왼쪽
                block_position[0] -= 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[0] += 1
            
            elif char == 'd': # 오른쪽
                block_position[0] += 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[0] -= 1

            elif char == 'w': # 회전
                rotated_block = rotate_clockwise(current_block_shape)
                if not check_collision(board, rotated_block, block_position):
                    current_block_shape = rotated_block

            elif char == 's': # 아래로
                block_position[1] += 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[1] -= 1
            
            elif char == ' ': # 하드 드롭
                while not check_collision(board, current_block_shape, block_position):
                    block_position[1] += 1
                block_position[1] -= 1
                board = place_block(board, current_block_shape, block_position)
                
                current_block_shape = TETROMINOS[random.choice(block_keys)]
                block_position = [3, 0]
                
                if check_collision(board, current_block_shape, block_position):
                    game_over = True
                gravity_timer = 0
            
            elif char == 'q': # 종료
                game_over = True

            # --- 중력 처리 ---
            if gravity_timer >= gravity_speed:
                gravity_timer = 0
                block_position[1] += 1
                if check_collision(board, current_block_shape, block_position):
                    block_position[1] -= 1
                    board = place_block(board, current_block_shape, block_position)
                    
                    current_block_shape = TETROMINOS[random.choice(block_keys)]
                    block_position = [3, 0]
                    
                    if check_collision(board, current_block_shape, block_position):
                        game_over = True
            
            # --- 렌더링 ---
            temp_board = [row[:] for row in board]
            temp_board = place_block(temp_board, current_block_shape, block_position)

            os.system('cls' if os.name == 'nt' else 'clear')
            print("--- 테트리스 게임 ---")
            draw_board(temp_board)
            print("조작: a(왼쪽), d(오른쪽), w(회전), s(아래로), 스페이스바(하드 드롭), q(종료)")
            
            time.sleep(0.1)

    print("--- GAME OVER ---")
    draw_board(board)


