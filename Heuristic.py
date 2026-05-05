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
def debug_change(heuristic, r, c, old, new):
    print(f"[{heuristic}] Row {r} col {c} changed {color_name(old)} -> {color_name(new)}")

'''
    Fill one random EMPTY cell with a random color (WHITE or BLACK).
    Returns True if a cell was filled, False if no EMPTY cells remain.
'''
def random_fill(board):
    rows = len(board)
    cols = len(board[0])

    empty_cells = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if board[r][c] == EMPTY
    ]

    if not empty_cells:
        return False, None, None

    r, c = random.choice(empty_cells)

    old = board[r][c]
    new = random.choice([WHITE, BLACK])
    board[r][c] = new

    debug_change("random_fill", r, c, old, new)

    return True, r, c

'''
    1. select the most constrained cells (row or column with the least EMPTY cell(s))
    2. from selected cells, select the most constrained (column or row with the least EMPTY cell(s))
    3. fill the selected cell with random 0/1
'''
def fill_most_constrained_cell(board):
    rows = len(board)
    cols = len(board[0])

    # Step 1: find row with minimum EMPTY (>0)
    min_empty_row = None
    min_empty_count = cols + 1

    for r in range(rows):
        empty_count = board[r].count(EMPTY)
        if 0 < empty_count < min_empty_count:
            min_empty_count = empty_count
            min_empty_row = r

    if min_empty_row is None:
        return False, None, None

    # Step 2: find best column
    candidates = [c for c in range(cols) if board[min_empty_row][c] == EMPTY]

    best_c = candidates[0]
    min_empty_col = rows + 1

    for c in candidates:
        col_empty_count = sum(1 for r in range(rows) if board[r][c] == EMPTY)
        if col_empty_count < min_empty_col:
            min_empty_col = col_empty_count
            best_c = c

    r, c = min_empty_row, best_c

    # Step 3: random fill only
    old = board[r][c]
    new = random.choice([WHITE, BLACK])
    board[r][c] = new

    debug_change("fill_most_constrained_cell", r, c, old, new)

    return True, r, c

'''
    1. select random EMPTY cell
    2. check neighbour in size h x w
    3. if the filled cells >= threshold, then randomly fill the cell with BLACK or WHITE
'''
def get_window_size(rows, cols):
    h = max(3, rows // 5)
    w = max(3, cols // 5)
    return h, w

def heuristic_density_fill(board, threshold=0.8, max_attempts=100):
    import random

    rows = len(board)
    cols = len(board[0])

    h, w = get_window_size(rows, cols)

    # select all EMPTY cell(s)
    empty_cells = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if board[r][c] == EMPTY
    ]

    if not empty_cells:
        return False, None, None

    attempts = 0

    while attempts < max_attempts:
        attempts += 1

        # select random cell
        r, c = random.choice(empty_cells)

        # set local window
        r_start = max(0, r - h // 2)
        c_start = max(0, c - w // 2)

        r_end = min(rows, r_start + h)
        c_end = min(cols, c_start + w)

        # count density
        filled = 0
        total = 0

        for i in range(r_start, r_end):
            for j in range(c_start, c_end):
                total += 1
                if board[i][j] != EMPTY:
                    filled += 1

        density = filled / total

        # if pass threshold, then fill
        if density >= threshold:
            old = board[r][c]
            new = random.choice([WHITE, BLACK])

            board[r][c] = new
            debug_change("density_fill", r, c, old, new)

            return True, r, c

    # if there is no candidate
    return False, None, None