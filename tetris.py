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

if __name__ == "__main__":
    # 새로운 빈 보드를 생성합니다.
    game_board = create_empty_board(BOARD_WIDTH, BOARD_HEIGHT)

    # 블록과 위치를 선택합니다.
    current_block = TETROMINOS['T']
    # 너비가 3인 블록을 중앙에 위치시킵니다. x = (10-3)//2 = 3
    block_position = (3, 0) 

    # 보드에 블록을 배치합니다.
    game_board = place_block(game_board, current_block, block_position)

    # 블록이 포함된 보드를 그립니다.
    print("--- 테트리스 게임 화면 ---")
    draw_board(game_board)


