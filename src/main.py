import time
import os
import sys
import tty
import termios
import select

# 게임 설정
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# 게임 보드 (0: 빈칸, 1: 블록)
board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# T-piece 블록 모양 (상대 좌표)
block_shape = [
    (0, 0), (1, 0), (2, 0),  # 가로줄
    (1, 1)                     # 아래 중앙
]

# 다음 블록 (미리보기용)
next_block_shape = [
    (0, 0), (1, 0), (2, 0),
    (1, 1)
]

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
    screen_buffer.append("Controls: ←/a=left, →/d=right, ↓/s=down, q=quit")

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
        elif key == 'q':
            running = False

        # 자동 낙하 (0.5초마다)
        current_time = time.time()
        if current_time - last_drop > 0.5:
            if not move_down():
                # 블록이 바닥에 닿으면 종료 (임시)
                running = False
            last_drop = current_time

        time.sleep(0.05)

finally:
    # 터미널 설정 복원
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print("\nGame Over!")