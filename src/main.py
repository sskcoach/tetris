import time
import os
import sys
import tty
import termios
import select
import random

# 게임 설정
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# 게임 보드 (0: 빈칸, 1: 블록)
board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# 테트리미노 블록 정의 (각 블록의 4가지 회전 상태)
TETROMINOS = {
    'I': [
        [(0, 1), (1, 1), (2, 1), (3, 1)],  # 가로
        [(2, 0), (2, 1), (2, 2), (2, 3)],  # 세로
        [(0, 2), (1, 2), (2, 2), (3, 2)],  # 가로
        [(1, 0), (1, 1), (1, 2), (1, 3)]   # 세로
    ],
    'O': [
        [(1, 0), (2, 0), (1, 1), (2, 1)],  # 정사각형 (회전 없음)
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)]
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],  # ㅗ
        [(1, 0), (1, 1), (2, 1), (1, 2)],  # ㅏ
        [(0, 1), (1, 1), (2, 1), (1, 2)],  # ㅜ
        [(1, 0), (0, 1), (1, 1), (1, 2)]   # ㅓ
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],  # ㄱㄱ
        [(1, 0), (1, 1), (2, 1), (2, 2)],  # ㅁㅁ
        [(1, 1), (2, 1), (0, 2), (1, 2)],  # ㄱㄱ
        [(0, 0), (0, 1), (1, 1), (1, 2)]   # ㅁㅁ
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],  # ㄴㄴ
        [(2, 0), (1, 1), (2, 1), (1, 2)],  # ㅁㅁ
        [(0, 1), (1, 1), (1, 2), (2, 2)],  # ㄴㄴ
        [(1, 0), (0, 1), (1, 1), (0, 2)]   # ㅁㅁ
    ],
    'J': [
        [(1, 0), (1, 1), (0, 2), (1, 2)],  # ㄱ
        [(0, 0), (0, 1), (1, 1), (2, 1)],  # ㄴ
        [(1, 0), (2, 0), (1, 1), (1, 2)],  # ㄱ
        [(0, 1), (1, 1), (2, 1), (2, 2)]   # ㄴ
    ],
    'L': [
        [(1, 0), (1, 1), (1, 2), (2, 2)],  # L
        [(0, 1), (1, 1), (2, 1), (0, 2)],  # ㄴ
        [(0, 0), (1, 0), (1, 1), (1, 2)],  # L
        [(2, 0), (0, 1), (1, 1), (2, 1)]   # ㄴ
    ]
}

def get_random_block():
    """랜덤 블록 타입과 회전 상태 반환"""
    block_type = random.choice(list(TETROMINOS.keys()))
    return block_type, 0  # (타입, 회전 상태)

# 현재 블록
current_block_type, current_rotation = get_random_block()
block_shape = list(TETROMINOS[current_block_type][current_rotation])

# 다음 블록 (미리보기용)
next_block_type, next_rotation = get_random_block()
next_block_shape = list(TETROMINOS[next_block_type][next_rotation])

# 블록 위치
block_x = 3
block_y = 0

def render():
    """게임 화면을 렌더링"""
    screen_buffer = []

    # 임시 보드 생성 (현재 블록 포함)
    temp_board = [row[:] for row in board]
    for dx, dy in block_shape:
        bx, by = block_x + dx, block_y + dy
        if 0 <= by < BOARD_HEIGHT and 0 <= bx < BOARD_WIDTH:
            temp_board[by][bx] = 1

    # 다음 블록 미리보기 보드 생성 (4x4)
    next_preview = [[0 for _ in range(4)] for _ in range(4)]
    for dx, dy in next_block_shape:
        if dx < 4 and dy < 4:
            next_preview[dy][dx] = 1

    # 보드를 문자열로 변환 (미리보기 포함)
    screen_buffer.append("              NEXT")

    for y in range(BOARD_HEIGHT):
        line = "<|"
        for x in range(BOARD_WIDTH):
            if temp_board[y][x] == 1:
                line += "[]"
            else:
                line += " ."
        line += "|>"

        # 다음 블록 미리보기 추가 (상단 4줄)
        if y == 1:
            line += "  ┌────────┐"
        elif y >= 2 and y <= 5:
            line += "  │"
            preview_y = y - 2
            for px in range(4):
                if next_preview[preview_y][px] == 1:
                    line += "[]"
                else:
                    line += "  "
            line += "│"
        elif y == 6:
            line += "  └────────┘"

        screen_buffer.append(line)

    # 하단 테두리
    screen_buffer.append("<|====================|>")
    screen_buffer.append(" \\/\\/\\/\\/\\/\\/\\/\\/\\/\\/\\/ ")
    screen_buffer.append("")
    screen_buffer.append("Controls: ←/a=left, →/d=right, ↓/s=down, ↑/w=rotate")
    screen_buffer.append("          SPACE=drop, q=quit")

    # 화면 클리어 후 출력
    os.system('clear' if os.name == 'posix' else 'cls')
    print('\n'.join(screen_buffer))

def get_key():
    """논블로킹 키 입력 (방향키 지원)"""
    if select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.read(1)

        # ESC 시퀀스 처리 (방향키)
        if ch == '\x1b':
            # 나머지 시퀀스를 즉시 읽기
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A':
                    return 'UP'
                elif ch3 == 'B':
                    return 'DOWN'
                elif ch3 == 'C':
                    return 'RIGHT'
                elif ch3 == 'D':
                    return 'LEFT'

        return ch
    return None

def can_move(dx, dy):
    """블록이 이동 가능한지 체크"""
    for bx, by in block_shape:
        new_x = block_x + bx + dx
        new_y = block_y + by + dy

        # 경계 체크
        if new_x < 0 or new_x >= BOARD_WIDTH:
            return False
        if new_y < 0 or new_y >= BOARD_HEIGHT:
            return False

        # 보드와 충돌 체크
        if board[new_y][new_x] == 1:
            return False

    return True

def move_left():
    """블록을 왼쪽으로 이동"""
    global block_x
    if can_move(-1, 0):
        block_x -= 1

def move_right():
    """블록을 오른쪽으로 이동"""
    global block_x
    if can_move(1, 0):
        block_x += 1

def move_down():
    """블록을 아래로 이동"""
    global block_y
    if can_move(0, 1):
        block_y += 1
        return True
    return False

def hard_drop():
    """블록을 바닥까지 즉시 떨어뜨림"""
    while move_down():
        pass
    return True

def rotate_block():
    """블록을 시계방향으로 90도 회전"""
    global block_shape, current_rotation

    # 다음 회전 상태 계산
    new_rotation = (current_rotation + 1) % 4
    rotated = list(TETROMINOS[current_block_type][new_rotation])

    # 회전 후 충돌 체크
    original_shape = block_shape
    original_rotation = current_rotation

    block_shape = rotated
    current_rotation = new_rotation

    if not can_move(0, 0):
        # 충돌하면 원래대로
        block_shape = original_shape
        current_rotation = original_rotation
        return False

    return True

def lock_block():
    """현재 블록을 보드에 고정"""
    for dx, dy in block_shape:
        bx, by = block_x + dx, block_y + dy
        if 0 <= by < BOARD_HEIGHT and 0 <= bx < BOARD_WIDTH:
            board[by][bx] = 1

def clear_lines():
    """완성된 줄을 제거하고 점수 반환"""
    lines_cleared = 0
    y = BOARD_HEIGHT - 1

    while y >= 0:
        # 현재 줄이 완전히 채워졌는지 확인
        if all(board[y][x] == 1 for x in range(BOARD_WIDTH)):
            # 줄 제거
            del board[y]
            # 맨 위에 빈 줄 추가
            board.insert(0, [0 for _ in range(BOARD_WIDTH)])
            lines_cleared += 1
            # 같은 y를 다시 체크 (위에서 내려온 줄)
        else:
            y -= 1

    return lines_cleared

def spawn_new_block():
    """새로운 블록 생성"""
    global block_x, block_y, block_shape, current_block_type, current_rotation
    global next_block_type, next_rotation, next_block_shape

    # 다음 블록을 현재 블록으로
    current_block_type = next_block_type
    current_rotation = next_rotation
    block_shape = list(TETROMINOS[current_block_type][current_rotation])
    block_x = 3
    block_y = 0

    # 새로운 다음 블록을 랜덤 생성
    next_block_type, next_rotation = get_random_block()
    next_block_shape = list(TETROMINOS[next_block_type][next_rotation])

    # 생성 위치에 블록이 있으면 게임오버
    if not can_move(0, 0):
        return False

    return True

# 터미널 체크
if not sys.stdin.isatty():
    print("Error: This game must be run in a terminal.")
    print("Please run: python src/main.py")
    sys.exit(1)

# 터미널 설정
old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())

    # 게임 루프
    last_drop = time.time()
    running = True

    while running:
        render()

        # 키 입력 처리
        key = get_key()
        if key == 'a' or key == 'LEFT':
            move_left()
        elif key == 'd' or key == 'RIGHT':
            move_right()
        elif key == 's' or key == 'DOWN':
            move_down()
        elif key == 'w' or key == 'UP':
            rotate_block()
        elif key == ' ':
            # 하드 드롭 (스페이스)
            hard_drop()
            lock_block()
            clear_lines()
            if not spawn_new_block():
                running = False
        elif key == 'q':
            running = False

        # 자동 낙하 (0.5초마다)
        current_time = time.time()
        if current_time - last_drop > 0.5:
            if not move_down():
                # 블록이 바닥에 닿으면 고정하고 새 블록 생성
                lock_block()
                clear_lines()  # 완성된 줄 제거
                if not spawn_new_block():
                    # 새 블록을 생성할 수 없으면 게임오버
                    running = False
            last_drop = current_time

        time.sleep(0.05)

finally:
    # 터미널 설정 복원
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print("\nGame Over!")