EMPTY = -1
WHITE = 0
BLACK = 1

'''
    Check if the board is locally valid (Binairo rules):
    - No more than half of each color in any row/column
    - No three consecutive identical colors
    - No duplicate rows/columns when fully filled
'''
def is_valid(board):
    size = len(board)
    half = size // 2

    # Check rows
    for r in range(size):
        row = board[r]

        # Rule: color count must not exceed half
        if row.count(WHITE) > half or row.count(BLACK) > half:
            return False

        # Rule: no three consecutive identical colors
        for c in range(size - 2):
            if row[c] == row[c+1] == row[c+2] != EMPTY:
                return False

    # Check columns
    for c in range(size):
        col = [board[r][c] for r in range(size)]

        if col.count(WHITE) > half or col.count(BLACK) > half:
            return False

        for r in range(size - 2):
            if col[r] == col[r+1] == col[r+2] != EMPTY:
                return False

    # OPTIONAL: UNIQUENESS CHECK (only for fully filled rows/columns)

    # Check unique rows
    full_rows = [tuple(row) for row in board if EMPTY not in row]
    if len(full_rows) != len(set(full_rows)):
        return False

    # Check unique columns
    cols = []
    for c in range(size):
        col = tuple(board[r][c] for r in range(size))
        if EMPTY not in col:
            cols.append(col)

    if len(cols) != len(set(cols)):
        return False

    return True