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

import os
import time
import random

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
                # 다른 블록과 충돌 확인
                if board[pos_y + r][pos_x + c] == '[]':
                    return True
    return False

if __name__ == "__main__":
    board = create_empty_board(BOARD_WIDTH, BOARD_HEIGHT)
    block_keys = list(TETROMINOS.keys())
    current_block_shape = TETROMINOS[random.choice(block_keys)]
    block_position = [3, 0] # 가변성을 위해 리스트 사용
    game_over = False

    while not game_over:
        # 1. 중력: 블록을 아래로 한 칸 이동
        block_position[1] += 1

        # 2. 충돌 확인
        if check_collision(board, current_block_shape, block_position):
            # 충돌 시, 블록을 이전 위치로 되돌림
            block_position[1] -= 1
            
            # 블록을 보드에 합침
            board = place_block(board, current_block_shape, block_position)
            
            # 새 블록 생성
            current_block_shape = TETROMINOS[random.choice(block_keys)]
            block_position = [3, 0]
            
            # 새 블록이 즉시 충돌하면 게임 오버
            if check_collision(board, current_block_shape, block_position):
                game_over = True

        # 3. 렌더링
        # 그리기를 위한 임시 보드 생성 (기존 보드는 그대로 유지)
        temp_board = [row[:] for row in board]
        
        # 현재 움직이는 블록을 임시 보드에 그림
        temp_board = place_block(temp_board, current_block_shape, block_position)

        # 화면을 지우고 보드 그리기
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- 테트리스 게임 화면 ---")
        draw_board(temp_board)
        
        # 4. 속도 조절
        time.sleep(0.5)

    print("--- GAME OVER ---")
    draw_board(board) # 최종 보드 상태를 보여줍니다.


