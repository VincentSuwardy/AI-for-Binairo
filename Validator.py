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
    rows = len(board)
    cols = len(board[0])

    # Check rows
    for r in range(rows):
        row = board[r]
        half = cols // 2

        # Rule: color count must not exceed half
        if row.count(WHITE) > half or row.count(BLACK) > half:
            return False

        # Rule: no three consecutive identical colors
        for c in range(cols - 2):
            if row[c] == row[c+1] == row[c+2] != EMPTY:
                return False

    # Check columns
    for c in range(cols):
        col = [board[r][c] for r in range(rows)]
        half = rows // 2

        if col.count(WHITE) > half or col.count(BLACK) > half:
            return False

        for r in range(rows - 2):
            if col[r] == col[r+1] == col[r+2] != EMPTY:
                return False

    # OPTIONAL: UNIQUENESS CHECK (only for fully filled rows/columns)

    # Check unique rows
    full_rows = [tuple(board[r]) for r in range(rows) if EMPTY not in board[r]]
    if len(full_rows) != len(set(full_rows)):
        return False

    # Check unique columns
    full_cols = []
    for c in range(cols):
        col = tuple(board[r][c] for r in range(rows))
        if EMPTY not in col:
            full_cols.append(col)

    if len(full_cols) != len(set(full_cols)):
        return False

    return True