EMPTY = -1
WHITE = 0
BLACK = 1

'''
    Apply constraint patterns to the puzzle board.
    @param board: 2D list of integers (-1 = empty, 0 = white, 1 = black)
    @return: Updated board after applying all possible rules
'''
def apply_constraints(board):
    size = len(board)
    changed = True

    while changed:
        changed = False

        # apply rules
        # changed |= pattern_0(board)
        changed |= pattern_1(board)
        changed |= pattern_2(board)
        changed |= pattern_3(board)
        # changed |= pattern_4(board)
        # changed |= pattern_5(board)
        # changed |= pattern_6(board)
        # changed |= pattern_7(board)

    return board

# random fills
'''
    Fill all empty cells with random colors (0 or 1).
    Used when no more deterministic constraints apply.
'''
def fill_random(board):
    import random
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c] == EMPTY:
                old = board[r][c]
                board[r][c] = random.choice([WHITE, BLACK])
                print(f"[fill_random] Row {r} col {c} changed {old} -> {board[r][c]}")
    return board

# game patterns
'''
    Pattern 0:
    - Each row and column must be unique.
    - No two rows or columns can be identical.
'''
def pattern_0(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed


'''
    Pattern 1:
    - No three consecutive cells can have the same color.
    - Close open ends of two consecutive identical tiles.

    Example:
    _ 0 0 _  →  1 0 0 1
'''
def pattern_1(board):
    size = len(board)
    changed = False

    # check rows
    for r in range(size):
        for c in range(size-2):
            triple = board[r][c:c+3]

            # If two same colors followed by an empty cell
            if triple[0] == triple[1] != EMPTY and triple[2] == EMPTY:
                old = board[r][c+2]
                board[r][c+2] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_1] Row {r} col {c+2} changed {old} -> {board[r][c+2]}")
                changed = True

            # If two same colors preceded by an empty cell
            if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                old = board[r][c]
                board[r][c] = WHITE if triple[1] == BLACK else BLACK
                print(f"[pattern_1] Row {r} col {c} changed {old} -> {board[r][c]}")
                changed = True

    # check columns
    for c in range(size):
        for r in range(size - 2):
            triple = [board[r+i][c] for i in range(3)]

            if triple[0] == triple[1] != EMPTY and triple[2] == EMPTY:
                old = board[r+2][c]
                board[r+2][c] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_1] Col {c} row {r+2} changed {old} -> {board[r+2][c]}")
                changed = True
            if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                old = board[r][c]
                board[r][c] = WHITE if triple[1] == BLACK else BLACK
                print(f"[pattern_1] Col {c} row {r} changed {old} -> {board[r][c]}")
                changed = True

    return changed


'''
    Pattern 2:
    - No three cells with the same color, even with one gap.
    - If two identical tiles are separated by one empty cell, fill the middle with the opposite color.

    Example:
    0 _ 0  →  0 1 0
'''
def pattern_2(board):
    size = len(board)
    changed = False

    # check rows
    for r in range(size):
        for c in range(size - 2):
            triple = board[r][c:c+3]
            if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                old = board[r][c+1]
                board[r][c+1] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_2] Row {r} col {c+1} changed {old} -> {board[r][c+1]}")
                changed = True

    # check columns
    for c in range(size):
        for r in range(size - 2):
            triple = [board[r+i][c] for i in range(3)]
            if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                old = board[r+1][c]
                board[r+1][c] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_2] Col {c} row {r+1} changed {old} -> {board[r+1][c]}")
                changed = True

    return changed


'''
    Pattern 3:
    Each row and column must contain an equal number of black and white tiles. Automatically fill the rest when one color reaches half of the row/column.
'''
def pattern_3(board):
    size = len(board)
    changed = False
    half = size // 2

    # check rows
    for r in range(size):
        row = board[r]
        if row.count(WHITE) == half:
            for c in range(size):
                if row[c] == EMPTY:
                    old = row[c]
                    row[c] = BLACK
                    print(f"[pattern_3] Row {r} col {c} changed {old} -> BLACK")
                    changed = True
        elif row.count(BLACK) == half:
            for c in range(size):
                if row[c] == EMPTY:
                    old = row[c]
                    row[c] = WHITE
                    print(f"[pattern_3] Row {r} col {c} changed {old} -> WHITE")
                    changed = True
    
    # check columns
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        if col.count(WHITE) == half:
            for r in range(size):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = BLACK
                    print(f"[pattern_3] Col {c} row {r} changed {old} -> BLACK")
                    changed = True
        elif col.count(BLACK) == half:
            for r in range(size):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = WHITE
                    print(f"[pattern_3] Col {c} row {r} changed {old} -> WHITE")
                    changed = True

    return changed

'''
    Pattern 4:

'''
def pattern_4(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed

'''
    Pattern 5:

'''
def pattern_5(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed

'''
    Pattern 6:

'''
def pattern_6(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed

'''
    Pattern 7:
    
'''
def pattern_7(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed
