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
        changed |= pattern_0(board)
        changed |= pattern_1(board)
        changed |= pattern_2(board)
        changed |= pattern_3(board)
        changed |= pattern_4(board)
        # changed |= pattern_5(board)
        # changed |= pattern_6(board)
        # changed |= pattern_7(board)

        # fill random
        # changed |= fill_random(board)

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
                print(f"[fill_rand] Row {r} col {c} changed {color_name(old)} -> {color_name(board[r][c])}")
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
    half = size // 2

    # check rows
    for r in range(size):
        row = board[r]
        if EMPTY not in row:
            continue    # skip full row

        count_white = row.count(WHITE)
        count_black = row.count(BLACK)

        # find all fully filled rows
        for ref_r in range(size):
            ref_row = board[ref_r]
            if EMPTY in ref_row:
                continue    # only compare with full row

            # check if all non-empty cell in this row is identically with ref_row
            identical = True
            for c in range(size):
                if row[c] != EMPTY and row[c] != ref_row[c]:
                    identical = False
                    break

            if not identical:
                continue

            # check color count
            target_color = None
            if count_white == half - 1:
                target_color = WHITE
            elif count_black == half - 1:
                target_color = BLACK

            if target_color is None:
                continue  # no color with only 1 piece left

            # fill all empty cell in position with opposite color in ref_row
            if row[c] == EMPTY and ref_row[c] == (BLACK if target_color == WHITE else WHITE):
                    old = row[c]
                    row[c] = target_color
                    print(f"[pattern_0] Row {r} col {c} changed {color_name(old)} -> {color_name(row[c])}")
                    changed = True

    # check columns
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        if EMPTY not in col:
            continue

        count_white = col.count(WHITE)
        count_black = col.count(BLACK)

        for ref_c in range(size):
            ref_col = [board[r][ref_c] for r in range(size)]
            if EMPTY in ref_col or ref_c == c:
                continue

            identical = True
            for r in range(size):
                if board[r][c] != EMPTY and board[r][c] != ref_col[r]:
                    identical = False
                    break

            if not identical:
                continue

            target_color = None
            if count_white == half - 1:
                target_color = WHITE
            elif count_black == half - 1:
                target_color = BLACK

            if target_color is None:
                continue

            for r in range(size):
                if board[r][c] == EMPTY and ref_col[r] == (BLACK if target_color == WHITE else WHITE):
                    old = board[r][c]
                    board[r][c] = target_color
                    print(f"[pattern_0] Col {c} row {r} changed {color_name(old)} -> {color_name(board[r][c])}")
                    changed = True


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
                print(f"[pattern_1] Row {r} col {c+2} changed {color_name(old)} -> {color_name(board[r][c+2])}")
                changed = True

            # If two same colors preceded by an empty cell
            if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                old = board[r][c]
                board[r][c] = WHITE if triple[1] == BLACK else BLACK
                print(f"[pattern_1] Row {r} col {c} changed {color_name(old)} -> {color_name(board[r][c])}")
                changed = True

    # check columns
    for c in range(size):
        for r in range(size - 2):
            triple = [board[r+i][c] for i in range(3)]

            if triple[0] == triple[1] != EMPTY and triple[2] == EMPTY:
                old = board[r+2][c]
                board[r+2][c] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_1] Col {c} row {r+2} changed {color_name(old)} -> {color_name(board[r+2][c])}")
                changed = True
            if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                old = board[r][c]
                board[r][c] = WHITE if triple[1] == BLACK else BLACK
                print(f"[pattern_1] Col {c} row {r} changed {color_name(old)} -> {color_name(board[r][c])}")
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
                print(f"[pattern_2] Row {r} col {c+1} changed {color_name(old)} -> {color_name(board[r][c+1])}")
                changed = True

    # check columns
    for c in range(size):
        for r in range(size - 2):
            triple = [board[r+i][c] for i in range(3)]
            if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                old = board[r+1][c]
                board[r+1][c] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_2] Col {c} row {r+1} changed {color_name(old)} -> {color_name(board[r+1][c])}")
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
                    print(f"[pattern_3] Row {r} col {c} changed {color_name(old)} -> BLACK")
                    changed = True
        elif row.count(BLACK) == half:
            for c in range(size):
                if row[c] == EMPTY:
                    old = row[c]
                    row[c] = WHITE
                    print(f"[pattern_3] Row {r} col {c} changed {color_name(old)} -> WHITE")
                    changed = True
    
    # check columns
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        if col.count(WHITE) == half:
            for r in range(size):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = BLACK
                    print(f"[pattern_3] Col {c} row {r} changed {color_name(old)} -> BLACK")
                    changed = True
        elif col.count(BLACK) == half:
            for r in range(size):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = WHITE
                    print(f"[pattern_3] Col {c} row {r} changed {color_name(old)} -> WHITE")
                    changed = True

    return changed

'''
    Pattern 4: specific case only

    1 _ _ 1 _ 0 1 1 0 1 1 0 (1 _ 0 _ 1) _ _ 1 
    check if 1 left with 1 piece, fill rest with 0
    1 0 0 1 0 0 1 1 0 1 1 0 1 _ 0 _ 1 0 0 1
'''
def pattern_4(board):
    size = len(board)
    changed = False

    def fill_remaining(line, exclude_idx, fill_color, r=None, is_row=True):
        nonlocal changed
        for i in range(size):
            if i not in exclude_idx and line[i] == EMPTY:
                old = line[i]
                line[i] = fill_color
                changed = True
                if is_row:
                    print(f"[pattern_4] Row {r} col {i} changed {color_name(old)} -> {color_name(fill_color)}")
                else:
                    print(f"[pattern_4] Col {r} row {i} changed {color_name(old)} -> {color_name(fill_color)}")

    # check rows
    for r in range(size):
        row = board[r]
        count_white = row.count(WHITE)
        count_black = row.count(BLACK)
        empty_count = row.count(EMPTY)
        half = size // 2

        # check both colors left
        white_left = half - count_white
        black_left = half - count_black

        # skip if both left with more or less than 1
        if white_left != 1 and black_left != 1:
            continue

        for c in range(size - 4):
            seg = row[c:c+5]

            # case: 1 _ 0 _ 1
            if seg[0] == seg[4] == BLACK and seg[2] == WHITE and seg[1] == seg[3] == EMPTY:
                if black_left == 1:  # only if BLACK left with 1 piece
                    fill_remaining(row, [c+1, c+3], WHITE, r, True)

            # case: 0 _ 1 _ 0
            elif seg[0] == seg[4] == WHITE and seg[2] == BLACK and seg[1] == seg[3] == EMPTY:
                if white_left == 1:  # only if WHITE left with 1 piece
                    fill_remaining(row, [c+1, c+3], BLACK, r, True)

    # check columns
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        count_white = col.count(WHITE)
        count_black = col.count(BLACK)
        empty_count = col.count(EMPTY)
        half = size // 2

        white_left = half - count_white
        black_left = half - count_black

        if white_left != 1 and black_left != 1:
            continue

        for r in range(size - 4):
            seg = col[r:r+5]

            # case: 1 _ 0 _ 1
            if seg[0] == seg[4] == BLACK and seg[2] == WHITE and seg[1] == seg[3] == EMPTY:
                if black_left == 1:
                    # fill all empty cell unless idx in pattern
                    fill_remaining(col, [r+1, r+3], WHITE, c, False)
                    # write back to board
                    for rr in range(size):
                        board[rr][c] = col[rr]

            # case: 0 _ 1 _ 0
            elif seg[0] == seg[4] == WHITE and seg[2] == BLACK and seg[1] == seg[3] == EMPTY:
                if white_left == 1:
                    fill_remaining(col, [r+1, r+3], BLACK, c, False)
                    for rr in range(size):
                        board[rr][c] = col[rr]
    
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
