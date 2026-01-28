import curses
import time
import random
import os
import subprocess
import threading

# Import BGM module
try:
    from music.tetris_bgm import (
        _generate_full_track_wav, TETRIS_SIMPLE, BASS_LINE
    )
    BGM_AVAILABLE = True
except ImportError:
    BGM_AVAILABLE = False

# BGM state
_bgm_playing = False
_bgm_process = None
_bgm_temp_file = '/tmp/tetris_game_bgm.wav'


def start_game_bgm(tempo=120):
    """Start background music for game"""
    global _bgm_playing, _bgm_process
    if not BGM_AVAILABLE or _bgm_playing:
        return

    # Generate BGM file in background thread to avoid blocking
    def generate_and_play():
        global _bgm_playing, _bgm_process
        try:
            wav_data, _ = _generate_full_track_wav(
                TETRIS_SIMPLE, BASS_LINE, tempo, repeats=10
            )
            with open(_bgm_temp_file, 'wb') as f:
                f.write(wav_data)

            # Play loop
            while _bgm_playing:
                _bgm_process = subprocess.Popen(
                    ['afplay', _bgm_temp_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                _bgm_process.wait()
                if not _bgm_playing:
                    break
        except Exception:
            pass

    _bgm_playing = True
    threading.Thread(target=generate_and_play, daemon=True).start()


def stop_game_bgm():
    """Stop background music"""
    global _bgm_playing, _bgm_process
    _bgm_playing = False

    # Kill the process directly
    if _bgm_process:
        try:
            _bgm_process.terminate()
            _bgm_process.kill()
        except Exception:
            pass
        _bgm_process = None

    # Also kill any stray afplay
    subprocess.Popen(['pkill', '-9', 'afplay'],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)

    # Clean up temp file (non-blocking)
    def cleanup():
        time.sleep(0.2)
        if os.path.exists(_bgm_temp_file):
            try:
                os.remove(_bgm_temp_file)
            except OSError:
                pass
    threading.Thread(target=cleanup, daemon=True).start()

# Game board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Board display offset
BOARD_OFFSET_Y = 1
BOARD_OFFSET_X = 1

# Board characters
BORDER_LEFT = "<!"
BORDER_RIGHT = "!>"
BOTTOM_BORDER_TOP = "=="
BOTTOM_BORDER_BOTTOM = r"\/"
EMPTY_CELL = " ."
BLOCK_CHAR = "[]"

# Color pairs for GREEN monitor style
COLOR_NORMAL = 1      # Normal green text
COLOR_BRIGHT = 2      # Bright green (blocks, important)
COLOR_DIM = 3         # Dim green (borders, background)
COLOR_TITLE = 4       # Title text


def init_colors():
    """Initialize GREEN monitor color scheme"""
    curses.start_color()
    curses.use_default_colors()

    # Define green shades
    curses.init_pair(COLOR_NORMAL, curses.COLOR_GREEN, -1)
    curses.init_pair(COLOR_BRIGHT, curses.COLOR_GREEN, -1)  # Will use A_BOLD
    curses.init_pair(COLOR_DIM, curses.COLOR_GREEN, -1)     # Will use A_DIM
    curses.init_pair(COLOR_TITLE, curses.COLOR_GREEN, -1)

# Tetromino shapes in their bounding boxes for rotation
TETROMINOES = {
    'I': [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]],
    'O': [[1,1], [1,1]],
    'T': [[0,1,0], [1,1,1], [0,0,0]],
    'L': [[0,0,1], [1,1,1], [0,0,0]],
    'J': [[1,0,0], [1,1,1], [0,0,0]],
    'S': [[0,1,1], [1,1,0], [0,0,0]],
    'Z': [[1,1,0], [0,1,1], [0,0,0]]
}
TETROMINO_NAMES = list(TETROMINOES.keys())

def rotate_piece(shape):
    transposed = list(zip(*shape))
    return [list(row) for row in reversed(transposed)]

def check_collision(board, piece_shape, piece_x, piece_y):
    for y, row in enumerate(piece_shape):
        for x, cell in enumerate(row):
            if cell:
                board_y, board_x = piece_y + y, piece_x + x
                if not (0 <= board_x < BOARD_WIDTH and 0 <= board_y < BOARD_HEIGHT) or \
                   (0 <= board_y < BOARD_HEIGHT and board[board_y][board_x] != 0):
                    return True
    return False

def lock_piece(board, piece_shape, piece_x, piece_y):
    for y, row in enumerate(piece_shape):
        for x, cell in enumerate(row):
            if cell and piece_y + y >= 0:
                board[piece_y + y][piece_x + x] = 1

def clear_lines(board):
    lines_cleared = 0
    y = BOARD_HEIGHT - 1
    while y >= 0:
        if all(cell != 0 for cell in board[y]):
            del board[y]
            board.insert(0, [0 for _ in range(BOARD_WIDTH)])
            lines_cleared += 1
        else:
            y -= 1
    return lines_cleared

def draw_text(stdscr, y, x, text, bright=False):
    if bright:
        stdscr.addstr(y, x, text, curses.color_pair(COLOR_BRIGHT) | curses.A_BOLD)
    else:
        stdscr.addstr(y, x, text, curses.color_pair(COLOR_NORMAL))

def draw_playfield(stdscr, board, board_offset_y, board_offset_x):
    dim_color = curses.color_pair(COLOR_DIM) | curses.A_DIM
    bright_color = curses.color_pair(COLOR_BRIGHT) | curses.A_BOLD

    for y in range(BOARD_HEIGHT):
        stdscr.addstr(board_offset_y + y, board_offset_x, BORDER_LEFT, dim_color)
        for x in range(BOARD_WIDTH):
            if board[y][x] != 0:
                stdscr.addstr(board_offset_y + y, board_offset_x + 2 + x * 2, BLOCK_CHAR, bright_color)
            else:
                stdscr.addstr(board_offset_y + y, board_offset_x + 2 + x * 2, EMPTY_CELL, dim_color)
        stdscr.addstr(board_offset_y + y, board_offset_x + 2 + BOARD_WIDTH * 2, BORDER_RIGHT, dim_color)
    bottom_y = board_offset_y + BOARD_HEIGHT
    stdscr.addstr(bottom_y, board_offset_x, "  " + BOTTOM_BORDER_TOP * BOARD_WIDTH + "  ", dim_color)
    stdscr.addstr(bottom_y + 1, board_offset_x, "  " + BOTTOM_BORDER_BOTTOM * BOARD_WIDTH + "  ", dim_color)

def draw_tetromino(stdscr, shape, piece_y, piece_x, board_offset_y, board_offset_x):
    screen_y = board_offset_y + piece_y
    screen_x = board_offset_x + 2 + piece_x * 2
    bright_color = curses.color_pair(COLOR_BRIGHT) | curses.A_BOLD
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                stdscr.addstr(screen_y + y, screen_x + x * 2, BLOCK_CHAR, bright_color)

def draw_preview_box(stdscr, next_piece_shape, board_offset_y, board_offset_x):
    preview_box_h, preview_box_w = 6, 12
    preview_offset_y = board_offset_y
    preview_offset_x = board_offset_x + (BOARD_WIDTH * 2) + 6
    dim_color = curses.color_pair(COLOR_DIM) | curses.A_DIM
    bright_color = curses.color_pair(COLOR_BRIGHT) | curses.A_BOLD
    normal_color = curses.color_pair(COLOR_NORMAL)

    stdscr.addstr(preview_offset_y, preview_offset_x, "NEXT", normal_color)
    for y in range(preview_box_h):
        stdscr.addstr(preview_offset_y + 1 + y, preview_offset_x - 1, "|            |", dim_color)
    piece_h, piece_w = len(next_piece_shape), len(next_piece_shape[0])
    piece_draw_y = preview_offset_y + 1 + (preview_box_h - piece_h) // 2
    piece_draw_x = preview_offset_x + (preview_box_w - piece_w * 2) // 2
    for y, row in enumerate(next_piece_shape):
        for x, cell in enumerate(row):
            if cell:
                stdscr.addstr(piece_draw_y + y, piece_draw_x + x * 2, BLOCK_CHAR, bright_color)

# --- Scene Functions ---

def run_title_scene(stdscr):
    term_h, term_w = stdscr.getmaxyx()
    title = "TETRIS"

    start_y = (term_h // 2) - 1
    start_x = (term_w - len(title)) // 2
    draw_text(stdscr, start_y, start_x, title, bright=True)

    prompt = "Press any key to continue"
    draw_text(stdscr, start_y + 2, (term_w - len(prompt)) // 2, prompt)

    stdscr.move(term_h - 1, term_w - 1)
    stdscr.nodelay(False)
    stdscr.getch()
    return "MENU"

def run_menu_scene(stdscr):
    term_h, term_w = stdscr.getmaxyx()
    menu_items = ["Start Game", "Leaderboard", "Quit"]
    current_selection = 0

    while True:
        stdscr.clear()
        for i, item in enumerate(menu_items):
            start_x = (term_w - len(item)) // 2
            if i == current_selection:
                # Selected: bright green with reverse
                stdscr.addstr(term_h // 2 + i, start_x, f"> {item} <",
                             curses.color_pair(COLOR_BRIGHT) | curses.A_BOLD)
            else:
                # Not selected: dim green
                stdscr.addstr(term_h // 2 + i, start_x, f"  {item}  ",
                             curses.color_pair(COLOR_DIM))

        stdscr.move(term_h - 1, term_w - 1)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(menu_items) - 1:
            current_selection += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_selection == 0: return "GAME"
            elif current_selection == 1: return "LEADERBOARD"
            else: return "QUIT"

def run_game_scene(stdscr):
    stdscr.nodelay(True)
    stdscr.timeout(50)

    # Start BGM
    start_game_bgm(tempo=120)

    # --- Game State Initialization ---
    board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    score = 0
    level = 1
    lines_cleared_total = 0
    lines_per_level = 10
    
    # --- Timing & Leveling Helper ---
    def get_fall_interval(current_level):
        return max(0.05, 0.6 - (current_level * 0.05))

    def update_state_after_clear(cleared_count, current_score, current_level, current_total_lines):
        """Updates score, level, and total lines based on lines cleared."""
        new_score = current_score + [0, 100, 300, 500, 800][cleared_count]
        new_total_lines = current_total_lines + cleared_count
        new_level = 1 + (new_total_lines // lines_per_level)
        
        updated_fall_interval = get_fall_interval(new_level)
        
        return new_score, new_level, new_total_lines, updated_fall_interval

    fall_interval = get_fall_interval(level)
    last_fall_time = time.time()
    
    # --- Layout Calculation ---
    term_h, term_w = stdscr.getmaxyx()
    board_h_visual, board_w_visual = BOARD_HEIGHT + 2, BOARD_WIDTH * 2 + 4
    board_offset_y = (term_h - board_h_visual) // 2
    board_offset_x = (term_w - board_w_visual - 14) // 2

    # --- Piece Initialization ---
    current_piece_shape = TETROMINOES[random.choice(TETROMINO_NAMES)]
    next_piece_shape = TETROMINOES[random.choice(TETROMINO_NAMES)]
    current_piece_y, current_piece_x = 0, (BOARD_WIDTH - len(current_piece_shape[0])) // 2

    while True:
        if check_collision(board, current_piece_shape, current_piece_x, current_piece_y):
            stop_game_bgm()  # Stop BGM on game over
            return score # Game Over

        key = stdscr.getch()
        if key == ord('q'):
            stop_game_bgm()  # Stop BGM on quit
            return "MENU"

        # --- Input Handling & Cheats ---
        if key == curses.KEY_UP:
            rotated = rotate_piece(current_piece_shape)
            if not check_collision(board, rotated, current_piece_x, current_piece_y):
                current_piece_shape = rotated
        elif key == curses.KEY_LEFT:
            if not check_collision(board, current_piece_shape, current_piece_x - 1, current_piece_y):
                current_piece_x -= 1
        elif key == curses.KEY_RIGHT:
            if not check_collision(board, current_piece_shape, current_piece_x + 1, current_piece_y):
                current_piece_x += 1
        elif key == ord(' '):
            while not check_collision(board, current_piece_shape, current_piece_x, current_piece_y + 1):
                current_piece_y += 1
            last_fall_time = 0
        elif key in [ord('1'), ord('2'), ord('3'), ord('4')]:
            num_to_clear = int(chr(key))
            for _ in range(num_to_clear):
                if len(board) > 0: del board[-1]; board.insert(0, [0] * BOARD_WIDTH)
            
            score, level, lines_cleared_total, fall_interval = update_state_after_clear(
                num_to_clear, score, level, lines_cleared_total)
        
        elif key == ord('c'): # Cheat: Change piece
            current_piece_idx = TETROMINO_NAMES.index(current_piece_name)
            
            # Find next valid piece
            for _ in range(len(TETROMINO_NAMES) - 1): # Try all other pieces
                current_piece_idx = (current_piece_idx + 1) % len(TETROMINO_NAMES)
                potential_name = TETROMINO_NAMES[current_piece_idx]
                potential_shape = TETROMINOES[potential_name]
                
                if not check_collision(board, potential_shape, current_piece_x, current_piece_y):
                    current_piece_name = potential_name
                    current_piece_shape = potential_shape
                    break

        if key == curses.KEY_DOWN:
            if not check_collision(board, current_piece_shape, current_piece_x, current_piece_y + 1):
                current_piece_y += 1
                last_fall_time = time.time()

        # --- Game Logic ---
        if time.time() - last_fall_time > fall_interval:
            if not check_collision(board, current_piece_shape, current_piece_x, current_piece_y + 1):
                current_piece_y += 1
                last_fall_time = time.time()
            else: # Piece has landed
                lock_piece(board, current_piece_shape, current_piece_x, current_piece_y)
                lines_cleared = clear_lines(board)
                
                if lines_cleared > 0:
                    score, level, lines_cleared_total, fall_interval = update_state_after_clear(
                        lines_cleared, score, level, lines_cleared_total)

                # Setup next piece
                current_piece_shape = next_piece_shape
                next_piece_shape = TETROMINOES[random.choice(TETROMINO_NAMES)]
                current_piece_y, current_piece_x = 0, (BOARD_WIDTH - len(current_piece_shape[0])) // 2

        # --- Drawing ---
        stdscr.clear()
        lines_to_next_level = lines_per_level - (lines_cleared_total % lines_per_level)
        if lines_to_next_level == lines_per_level and lines_cleared_total != 0: # If it's a perfect multiple and not 0, it means we just leveled up or are at start
             lines_to_next_level = lines_per_level
        elif lines_cleared_total == 0:
            lines_to_next_level = lines_per_level # Start at 10 lines to next level

        info_text = f"Score: {score}  |  Level: {level}  |  Lines: {lines_to_next_level}"
        stdscr.addstr(board_offset_y - 2, board_offset_x, info_text,
                     curses.color_pair(COLOR_NORMAL))
        draw_playfield(stdscr, board, board_offset_y, board_offset_x)
        draw_tetromino(stdscr, current_piece_shape, current_piece_y, current_piece_x, board_offset_y, board_offset_x)
        draw_preview_box(stdscr, next_piece_shape, board_offset_y, board_offset_x)
        stdscr.move(term_h - 1, term_w - 1)
        stdscr.refresh()

LEADERBOARD_FILE = "leaderboard.txt"

def save_score(score):
    """Appends a score to the leaderboard file."""
    if score > 0:
        with open(LEADERBOARD_FILE, "a") as f:
            f.write(f"{score}\n")

def load_scores():
    """Loads scores from the file, sorts them, and returns the top 10."""
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
        scores.sort(reverse=True)
        return scores[:10]
    except FileNotFoundError:
        return []

def run_game_over_scene(stdscr, score):
    stop_game_bgm()  # Ensure BGM is stopped
    save_score(score) # Save the score
    term_h, term_w = stdscr.getmaxyx()
    msg1 = "GAME OVER"
    msg2 = f"Final Score: {score}"
    msg3 = "Press any key to return to menu"
    draw_text(stdscr, term_h // 2 - 1, (term_w - len(msg1)) // 2, msg1, bright=True)
    draw_text(stdscr, term_h // 2, (term_w - len(msg2)) // 2, msg2, bright=True)
    draw_text(stdscr, term_h // 2 + 2, (term_w - len(msg3)) // 2, msg3)
    
    stdscr.move(term_h - 1, term_w - 1)
    stdscr.nodelay(False)
    stdscr.getch()
    return "MENU"

def run_leaderboard_scene(stdscr):
    term_h, term_w = stdscr.getmaxyx()
    scores = load_scores()

    title = "--- LEADERBOARD ---"
    draw_text(stdscr, term_h // 2 - 7, (term_w - len(title)) // 2, title, bright=True)

    if not scores:
        no_scores_msg = "No scores yet. Play a game!"
        draw_text(stdscr, term_h // 2 - 5, (term_w - len(no_scores_msg)) // 2, no_scores_msg)
    else:
        for i, score in enumerate(scores):
            score_text = f"{i + 1}. {score}"
            # Top 3 scores are bright
            draw_text(stdscr, term_h // 2 - 5 + i, (term_w - len(score_text)) // 2,
                     score_text, bright=(i < 3))
            if i >= 9:
                break
    
    prompt = "Press any key to return to menu."
    draw_text(stdscr, term_h // 2 + 5, (term_w - len(prompt)) // 2, prompt)

    stdscr.move(term_h - 1, term_w - 1)
    stdscr.nodelay(False)
    stdscr.getch()
    return "MENU"

def main(stdscr):
    try: curses.curs_set(0)
    except curses.error: pass

    # Initialize GREEN monitor colors
    init_colors()

    current_scene = "TITLE"
    last_score = 0
    
    while current_scene != "QUIT":
        stdscr.clear()
        
        if current_scene == "TITLE":
            current_scene = run_title_scene(stdscr)
        elif current_scene == "MENU":
            current_scene = run_menu_scene(stdscr)
        elif current_scene == "GAME":
            last_score = run_game_scene(stdscr)
            current_scene = "GAME_OVER"
        elif current_scene == "GAME_OVER":
            current_scene = run_game_over_scene(stdscr, last_score)
        elif current_scene == "LEADERBOARD":
            current_scene = run_leaderboard_scene(stdscr)
        
        stdscr.refresh()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    finally:
        # Always stop BGM on exit
        stop_game_bgm()
