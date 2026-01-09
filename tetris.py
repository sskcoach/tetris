import curses
import time
import random

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

def draw_text(stdscr, y, x, text):
    stdscr.addstr(y, x, text)

def draw_playfield(stdscr, board, board_offset_y, board_offset_x):
    for y in range(BOARD_HEIGHT):
        stdscr.addstr(board_offset_y + y, board_offset_x, BORDER_LEFT)
        for x in range(BOARD_WIDTH):
            cell_char = BLOCK_CHAR if board[y][x] != 0 else EMPTY_CELL
            stdscr.addstr(board_offset_y + y, board_offset_x + 2 + x * 2, cell_char)
        stdscr.addstr(board_offset_y + y, board_offset_x + 2 + BOARD_WIDTH * 2, BORDER_RIGHT)
    bottom_y = board_offset_y + BOARD_HEIGHT
    stdscr.addstr(bottom_y, board_offset_x, "  " + BOTTOM_BORDER_TOP * BOARD_WIDTH + "  ")
    stdscr.addstr(bottom_y + 1, board_offset_x, "  " + BOTTOM_BORDER_BOTTOM * BOARD_WIDTH + "  ")

def draw_tetromino(stdscr, shape, piece_y, piece_x, board_offset_y, board_offset_x):
    screen_y = board_offset_y + piece_y
    screen_x = board_offset_x + 2 + piece_x * 2
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                stdscr.addstr(screen_y + y, screen_x + x * 2, BLOCK_CHAR)

def draw_preview_box(stdscr, next_piece_shape, board_offset_y, board_offset_x):
    preview_box_h, preview_box_w = 6, 12
    preview_offset_y = board_offset_y
    preview_offset_x = board_offset_x + (BOARD_WIDTH * 2) + 6
    stdscr.addstr(preview_offset_y, preview_offset_x, "NEXT")
    for y in range(preview_box_h):
        stdscr.addstr(preview_offset_y + 1 + y, preview_offset_x - 1, "|            |")
    piece_h, piece_w = len(next_piece_shape), len(next_piece_shape[0])
    piece_draw_y = preview_offset_y + 1 + (preview_box_h - piece_h) // 2
    piece_draw_x = preview_offset_x + (preview_box_w - piece_w * 2) // 2
    for y, row in enumerate(next_piece_shape):
        for x, cell in enumerate(row):
            if cell:
                stdscr.addstr(piece_draw_y + y, piece_draw_x + x * 2, BLOCK_CHAR)

# --- Scene Functions ---

def run_title_scene(stdscr):
    term_h, term_w = stdscr.getmaxyx()
    title = "TETRIS"
    
    start_y = (term_h // 2) - 1
    start_x = (term_w - len(title)) // 2
    draw_text(stdscr, start_y, start_x, title)
    
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
                stdscr.attron(curses.A_REVERSE)
                draw_text(stdscr, term_h // 2 + i, start_x, item)
                stdscr.attroff(curses.A_REVERSE)
            else:
                draw_text(stdscr, term_h // 2 + i, start_x, item)
        
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
            return score # Game Over

        key = stdscr.getch()
        if key == ord('q'): return "MENU"

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
        stdscr.addstr(board_offset_y - 2, board_offset_x, info_text)
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
    save_score(score) # Save the score
    term_h, term_w = stdscr.getmaxyx()
    msg1 = "GAME OVER"
    msg2 = f"Final Score: {score}"
    msg3 = "Press any key to return to menu"
    draw_text(stdscr, term_h // 2 - 1, (term_w - len(msg1)) // 2, msg1)
    draw_text(stdscr, term_h // 2, (term_w - len(msg2)) // 2, msg2)
    draw_text(stdscr, term_h // 2 + 2, (term_w - len(msg3)) // 2, msg3)
    
    stdscr.move(term_h - 1, term_w - 1)
    stdscr.nodelay(False)
    stdscr.getch()
    return "MENU"

def run_leaderboard_scene(stdscr):
    term_h, term_w = stdscr.getmaxyx()
    scores = load_scores()
    
    title = "--- LEADERBOARD ---"
    draw_text(stdscr, term_h // 2 - 7, (term_w - len(title)) // 2, title)

    if not scores:
        no_scores_msg = "No scores yet. Play a game!"
        draw_text(stdscr, term_h // 2 - 5, (term_w - len(no_scores_msg)) // 2, no_scores_msg)
    else:
        for i, score in enumerate(scores):
            score_text = f"{i + 1}. {score}"
            draw_text(stdscr, term_h // 2 - 5 + i, (term_w - len(score_text)) // 2, score_text)
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
    curses.wrapper(main)
