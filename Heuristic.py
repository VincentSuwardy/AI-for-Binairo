import random

EMPTY = -1
WHITE = 0
BLACK = 1

# DEBUGGING PURPOSE FUNCTION
def color_name(value):
    if value == WHITE:
        return "WHITE"
    elif value == BLACK:
        return "BLACK"
    else:
        return "EMPTY"

# DEBUG HELPER
def debug_change(pattern, r, c, old, new):
    print(f"[{pattern}] Row {r} col {c} changed {color_name(old)} -> {color_name(new)}")

'''
    Fill one random EMPTY cell with a random color (WHITE or BLACK).
    Returns True if a cell was filled, False if no EMPTY cells remain.
'''
def random_fill(board):
    size = len(board)

    empty_cells = [
        (r, c)
        for r in range(size)
        for c in range(size)
        if board[r][c] == EMPTY
    ]

    if not empty_cells:
        return False

    r, c = random.choice(empty_cells)

    old = board[r][c]
    new = random.choice([WHITE, BLACK])
    board[r][c] = new

    debug_change("random_fill", r, c, old, new)

    return True

'''
    1. Selalu pilih cell yang paling “terbatas” dulu, yaitu row atau column dengan jumlah EMPTY paling sedikit
    2. Dari kolom/kumpulan cell kosong itu, pilih cell yang paling terbatas lagi (EMPTY paling sedikit di kolom)
    3. Baru isi dengan random 0/1
'''
def fill_most_constrained_cell(board):
    size = len(board)

    # Step 1: find row with minimum EMPTY (>0)
    min_empty_row = None
    min_empty_count = size + 1

    for r in range(size):
        empty_count = board[r].count(EMPTY)
        if 0 < empty_count < min_empty_count:
            min_empty_count = empty_count
            min_empty_row = r

    if min_empty_row is None:
        return False

    # Step 2: find best column
    candidates = [c for c in range(size) if board[min_empty_row][c] == EMPTY]

    best_c = candidates[0]
    min_empty_col = size + 1

    for c in candidates:
        col_empty_count = sum(1 for r in range(size) if board[r][c] == EMPTY)
        if col_empty_count < min_empty_col:
            min_empty_col = col_empty_count
            best_c = c

    r, c = min_empty_row, best_c

    # Step 3: RANDOM FILL ONLY
    old = board[r][c]
    new = random.choice([WHITE, BLACK])
    board[r][c] = new

    debug_change("fill_most_constrained_cell", r, c, old, new)

    return True