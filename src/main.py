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

# 게임 씬
SCENE_SPLASH = 0
SCENE_TITLE = 1
SCENE_GAME = 2
SCENE_GAME_OVER = 3

current_scene = SCENE_SPLASH
splash_start_time = None

# 게임 보드 (0: 빈칸, 1: 블록)
board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

# 스테이지 정보
current_stage = 1
lines_to_clear = 1  # 스테이지 클리어에 필요한 줄 수

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

def render_splash():
    """스플래시 화면 렌더링"""
    screen_buffer = []
    screen_buffer.append("")
    screen_buffer.append("")
    screen_buffer.append("")
    screen_buffer.append("    ████████╗███████╗████████╗██████╗ ██╗███████╗")
    screen_buffer.append("    ╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝")
    screen_buffer.append("       ██║   █████╗     ██║   ██████╔╝██║███████╗")
    screen_buffer.append("       ██║   ██╔══╝     ██║   ██╔══██╗██║╚════██║")
    screen_buffer.append("       ██║   ███████╗   ██║   ██║  ██║██║███████║")
    screen_buffer.append("       ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝")
    screen_buffer.append("")
    screen_buffer.append("")
    screen_buffer.append("                   Loading...")
    screen_buffer.append("")

    print('\033[H\033[J' + '\n'.join(screen_buffer), end='', flush=True)

def render_title():
    """타이틀 화면 렌더링"""
    screen_buffer = []
    screen_buffer.append("")
    screen_buffer.append("")
    screen_buffer.append("    ████████╗███████╗████████╗██████╗ ██╗███████╗")
    screen_buffer.append("    ╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██║██╔════╝")
    screen_buffer.append("       ██║   █████╗     ██║   ██████╔╝██║███████╗")
    screen_buffer.append("       ██║   ██╔══╝     ██║   ██╔══██╗██║╚════██║")
    screen_buffer.append("       ██║   ███████╗   ██║   ██║  ██║██║███████║")
    screen_buffer.append("       ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝")
    screen_buffer.append("")
    screen_buffer.append("")
    screen_buffer.append("                Press SPACE to start")
    screen_buffer.append("                Press Q to quit")
    screen_buffer.append("")

    print('\033[H\033[J' + '\n'.join(screen_buffer), end='', flush=True)

def render_game():
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
    screen_buffer.append(f"   STAGE {current_stage}   NEXT")

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

    # 화면 클리어 후 출력 (ANSI escape code 사용으로 깜빡임 방지)
    print('\033[H\033[J' + '\n'.join(screen_buffer), end='', flush=True)

def render_game_over():
    """게임 오버 화면 렌더링"""
    screen_buffer = []
    screen_buffer.append("")
    screen_buffer.append("")
    screen_buffer.append("")
    screen_buffer.append("     ██████╗  █████╗ ███╗   ███╗███████╗")
    screen_buffer.append("    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝")
    screen_buffer.append("    ██║  ███╗███████║██╔████╔██║█████╗")
    screen_buffer.append("    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝")
    screen_buffer.append("    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗")
    screen_buffer.append("     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝")
    screen_buffer.append("")
    screen_buffer.append("      ██████╗ ██╗   ██╗███████╗██████╗")
    screen_buffer.append("     ██╔═══██╗██║   ██║██╔════╝██╔══██╗")
    screen_buffer.append("     ██║   ██║██║   ██║█████╗  ██████╔╝")
    screen_buffer.append("     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗")
    screen_buffer.append("     ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║")
    screen_buffer.append("      ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝")
    screen_buffer.append("")
    screen_buffer.append(f"             STAGE {current_stage} REACHED")
    screen_buffer.append("")
    screen_buffer.append("          Press SPACE to restart")
    screen_buffer.append("          Press Q to quit")
    screen_buffer.append("")

    print('\033[H\033[J' + '\n'.join(screen_buffer), end='', flush=True)

def render():
    """현재 씬에 따라 화면 렌더링"""
    if current_scene == SCENE_SPLASH:
        render_splash()
    elif current_scene == SCENE_TITLE:
        render_title()
    elif current_scene == SCENE_GAME:
        render_game()
    elif current_scene == SCENE_GAME_OVER:
        render_game_over()

def get_key():
    """논블로킹 키 입력 (방향키 지원, 버퍼 클리어)"""
    last_key = None

    # 버퍼에 쌓인 모든 입력을 읽어서 마지막 것만 사용
    while select.select([sys.stdin], [], [], 0)[0]:
        ch = sys.stdin.read(1)

        # ESC 시퀀스 처리 (방향키)
        if ch == '\x1b':
            # 나머지 시퀀스를 즉시 읽기
            ch2 = sys.stdin.read(1)
            if ch2 == '[':
                ch3 = sys.stdin.read(1)
                if ch3 == 'A':
                    last_key = 'UP'
                elif ch3 == 'B':
                    last_key = 'DOWN'
                elif ch3 == 'C':
                    last_key = 'RIGHT'
                elif ch3 == 'D':
                    last_key = 'LEFT'
        else:
            last_key = ch

    return last_key

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
    """완성된 줄을 제거하고 스테이지 클리어 여부 반환"""
    global current_stage, lines_to_clear

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

    # 스테이지 클리어 체크
    if lines_cleared >= lines_to_clear:
        return True  # 스테이지 클리어

    return False

def next_stage():
    """다음 스테이지로 진행"""
    global current_stage, board

    current_stage += 1

    # 보드 초기화
    board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

    return True

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

def reset_game():
    """게임 초기화"""
    global board, current_stage, block_x, block_y, block_shape, current_block_type, current_rotation
    global next_block_type, next_rotation, next_block_shape

    # 보드 초기화
    board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    current_stage = 1

    # 블록 초기화
    current_block_type, current_rotation = get_random_block()
    block_shape = list(TETROMINOS[current_block_type][current_rotation])
    next_block_type, next_rotation = get_random_block()
    next_block_shape = list(TETROMINOS[next_block_type][next_rotation])
    block_x = 3
    block_y = 0

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
    splash_start_time = time.time()

    while running:
        render()
        current_time = time.time()

        # 씬별 처리
        if current_scene == SCENE_SPLASH:
            # 스플래시는 2초 후 자동으로 타이틀로 전환
            if current_time - splash_start_time > 2.0:
                current_scene = SCENE_TITLE
            time.sleep(0.05)

        elif current_scene == SCENE_TITLE:
            # 타이틀 화면 키 입력
            key = get_key()
            if key == ' ':
                reset_game()
                current_scene = SCENE_GAME
                last_drop = current_time
            elif key == 'q':
                running = False
            time.sleep(0.05)

        elif current_scene == SCENE_GAME:
            # 게임 플레이 키 입력 처리
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
                stage_cleared = clear_lines()
                if stage_cleared:
                    next_stage()
                if not spawn_new_block():
                    current_scene = SCENE_GAME_OVER
            elif key == 'q':
                running = False

            # 자동 낙하 (0.5초마다)
            if current_time - last_drop > 0.5:
                if not move_down():
                    # 블록이 바닥에 닿으면 고정하고 새 블록 생성
                    lock_block()
                    stage_cleared = clear_lines()  # 완성된 줄 제거
                    if stage_cleared:
                        next_stage()
                    if not spawn_new_block():
                        # 새 블록을 생성할 수 없으면 게임오버
                        current_scene = SCENE_GAME_OVER
                last_drop = current_time

            time.sleep(0.05)

        elif current_scene == SCENE_GAME_OVER:
            # 게임 오버 화면 키 입력
            key = get_key()
            if key == ' ':
                reset_game()
                current_scene = SCENE_GAME
                last_drop = current_time
            elif key == 'q':
                running = False
            time.sleep(0.05)

finally:
    # 터미널 설정 복원
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print("\n\nThanks for playing!")