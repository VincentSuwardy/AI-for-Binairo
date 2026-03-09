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
    Apply constraint patterns to the puzzle board.
    @param board: 2D list of integers (-1 = empty, 0 = white, 1 = black)
    @return: Updated board after applying all possible rules
'''
def apply_constraints(board, difficulty):
    changed = True

    while changed:
        changed = False

        # apply rules
        changed |= pattern_1(board)
        changed |= pattern_2a(board)
        changed |= pattern_2b(board)

        if difficulty in ["hard", None]:
            changed |= pattern_3(board)
            changed |= pattern_4(board)
            changed |= pattern_5(board)
            changed |= pattern_6(board)
            changed |= pattern_7(board)
            changed |= pattern_8(board)

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
                debug_change("fill_random", r, c, old, board[r][c])
    return board

# game patterns
'''
    Pattern 1: Color Balancing
    Each row and column must contain an equal number of black and white tiles. Automatically fill the rest when one color reaches half of the row/column.
'''
def pattern_1(board):
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
                    debug_change("pattern_1", r, c, old, row[c])
                    changed = True
        elif row.count(BLACK) == half:
            for c in range(size):
                if row[c] == EMPTY:
                    old = row[c]
                    row[c] = WHITE
                    debug_change("pattern_1", r, c, old, row[c])
                    changed = True
    
    # check columns
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        if col.count(WHITE) == half:
            for r in range(size):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = BLACK
                    debug_change("pattern_1", r, c, old, board[r][c])
                    changed = True
        elif col.count(BLACK) == half:
            for r in range(size):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = WHITE
                    debug_change("pattern_1", r, c, old, board[r][c])
                    changed = True

    return changed


'''
    Pattern 2a: Three Adjacent
    - No three consecutive cells can have the same color.
    - Close open ends of two consecutive identical tiles.

    Example:
    _ 0 0 _  →  1 0 0 1
'''
def pattern_2a(board):
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
                debug_change("pattern_2a", r, c+2, old, board[r][c+2])
                changed = True

            # If two same colors preceded by an empty cell
            if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                old = board[r][c]
                board[r][c] = WHITE if triple[1] == BLACK else BLACK
                debug_change("pattern_2a", r, c, old, board[r][c])
                changed = True

    # check columns
    for c in range(size):
        for r in range(size - 2):
            triple = [board[r+i][c] for i in range(3)]

            if triple[0] == triple[1] != EMPTY and triple[2] == EMPTY:
                old = board[r+2][c]
                board[r+2][c] = WHITE if triple[0] == BLACK else BLACK
                debug_change("pattern_2a", r+2, c, old, board[r+2][c])
                changed = True
            if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                old = board[r][c]
                board[r][c] = WHITE if triple[1] == BLACK else BLACK
                debug_change("pattern_2a", r, c, old, board[r][c])
                changed = True

    return changed


'''
    Pattern 2b: Three Adjacent
    - No three cells with the same color, even with one gap.
    - If two identical tiles are separated by one empty cell, fill the middle with the opposite color.

    Example:
    0 _ 0  →  0 1 0
'''
def pattern_2b(board):
    size = len(board)
    changed = False

    # check rows
    for r in range(size):
        for c in range(size - 2):
            triple = board[r][c:c+3]
            if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                old = board[r][c+1]
                board[r][c+1] = WHITE if triple[0] == BLACK else BLACK
                debug_change("pattern_2b", r, c+1, old, board[r][c+1])
                changed = True

    # check columns
    for c in range(size):
        for r in range(size - 2):
            triple = [board[r+i][c] for i in range(3)]
            if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                old = board[r+1][c]
                board[r+1][c] = WHITE if triple[0] == BLACK else BLACK
                debug_change("pattern_2b", r+1, c, old, board[r+1][c])
                changed = True

    return changed


'''
    Pattern 3: Uniqueness
    - Each row and column must be unique.
    - No two rows or columns can be identical.
'''
def pattern_3(board):
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
                    debug_change("pattern_3", r, c, old, row[c])
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
                    debug_change("pattern_3", r, c, old, board[r][c])
                    changed = True


    return changed


'''
    Pattern 4: Absolute One
    check if one color has only 1 piece left, then fill the rest with the opposite color

    1 _ _ 1 _ 0 1 1 0 1 1 0 (1 _ 0 _ 1) _ _ 1 
    1 0 0 1 0 0 1 1 0 1 1 0 (1 _ 0 _ 1) 0 0 1
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
                    debug_change("pattern_4", r, i, old, fill_color)
                else:
                    debug_change("pattern_4", i, r, old, fill_color)

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
    Pattern 5: A Third Balance Filling
    check if the remaining pieces have a 1:3 ratio

    find 4 adjacent EMPTY cells
    0 0 1 0 0 1 1 0 _ _ _ _ 0 1 1 0 0 1 1 0

    fill the edge cells with the color that has 3 pieces left
    0 0 1 0 0 1 1 0 1 _ _ 1 0 1 1 0 0 1 1 0
'''
def pattern_5(board):
    size = len(board)
    half = size // 2
    changed = False

    # check rows
    for r in range(size):
        row = board[r]
        count_white = row.count(WHITE)
        count_black = row.count(BLACK)
        white_left = half - count_white
        black_left = half - count_black

        # check ratio 1:3
        if sorted([white_left, black_left]) == [1, 3]:
            color3 = BLACK if black_left == 3 else WHITE

            # check if there are 4 EMPTY that adjacent
            for i in range(size - 3):
                if all(row[i + j] == EMPTY for j in range(4)):
                    # fill left egde
                    if row[i] == EMPTY:
                        old = row[i]
                        row[i] = color3
                        debug_change("pattern_5", r, i, old, row[i])
                        changed = True
                    # fill right edge
                    if row[i + 3] == EMPTY:
                        old = row[i + 3]
                        row[i + 3] = color3
                        debug_change("pattern_5", r, i+3, old, row[i+3])
                        changed = True

    # check columns
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        count_white = col.count(WHITE)
        count_black = col.count(BLACK)
        white_left = half - count_white
        black_left = half - count_black

        if sorted([white_left, black_left]) == [1, 3]:
            color3 = BLACK if black_left == 3 else WHITE

            for i in range(size - 3):
                if all(col[i + j] == EMPTY for j in range(4)):
                    # fill top edge
                    if col[i] == EMPTY:
                        old = col[i]
                        col[i] = color3
                        debug_change("pattern_5", i, c, old, col[i])
                        changed = True
                    # fill bottom egde
                    if col[i + 3] == EMPTY:
                        old = col[i + 3]
                        col[i + 3] = color3
                        debug_change("pattern_5", i+3, c, old, col[i+3])
                        changed = True

        # rewrite to board
        for r in range(size):
            board[r][c] = col[r]

    return changed


def pattern_6(board):
    """
    Pattern 6: Forced Outside Fill
    If color X has exactly 1 tile left to place in a row/column
    and we detect a segment: X _ _ _ X
    then:
      - DO NOT fill the inside yet
      - fill ALL remaining EMPTY cells OUTSIDE the segment with opposite color Y

    This ensures the gap will not accidentally be filled with Y later,
    preventing illegal configuration: X Y Y Y X
    """
    size = len(board)
    half = size // 2
    changed = False

    def outside_fill(line, idx_start, idx_end, X):
        nonlocal changed
        Y = WHITE if X == BLACK else BLACK
        for i in range(size):
            if not (idx_start <= i <= idx_end):  # strictly outside the segment
                if line[i] == EMPTY:
                    old = line[i]
                    line[i] = Y
                    changed = True
                    debug_change("pattern_6", r_or_c, i if is_row else r_or_c, old, line[i])

    # check rows
    for r in range(size):
        row = board[r]
        count_white = row.count(WHITE)
        count_black = row.count(BLACK)
        white_left = half - count_white
        black_left = half - count_black

        if white_left == 1 or black_left == 1:
            X = WHITE if white_left == 1 else BLACK
            for i in range(size - 4):
                seg = row[i:i + 5]
                if seg[0] == X and seg[4] == X and seg[1] == seg[2] == seg[3] == EMPTY:
                    r_or_c = r  # debug index
                    is_row = True
                    outside_fill(row, i, i + 4, X)

    # check columns
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        count_white = col.count(WHITE)
        count_black = col.count(BLACK)
        white_left = half - count_white
        black_left = half - count_black

        if white_left == 1 or black_left == 1:
            X = WHITE if white_left == 1 else BLACK
            for i in range(size - 4):
                seg = col[i:i + 5]
                if seg[0] == X and seg[4] == X and seg[1] == seg[2] == seg[3] == EMPTY:
                    r_or_c = c
                    is_row = False
                    outside_fill(col, i, i + 4, X)
                    for r in range(size):
                        board[r][c] = col[r]

    return changed


'''
    Pattern 7: Double-Anchor Rule
    5-cell pattern with 1 remaining color

    if only one color (A) has 1 piece left,
    and the opposite color (B) still has more than 1 piece,
    find sequences with the pattern:

        A _ _ _ A

    then fill the center cell with the opposite color (B):

        A _ B _ A
'''
def pattern_7(board):
    size = len(board)
    changed = False

    half = size // 2

    for is_row in [True, False]:  # check both rows and columns
        for idx in range(size):
            line = board[idx] if is_row else [board[r][idx] for r in range(size)]

            # count remaining pieces
            count_white = line.count(WHITE)
            count_black = line.count(BLACK)
            white_left = half - count_white
            black_left = half - count_black

            # only proceed if one color has exactly 1 left
            if (white_left == 1 and black_left > 1) or (black_left == 1 and white_left > 1):
                target = WHITE if white_left == 1 else BLACK  # A
                opposite = BLACK if target == WHITE else WHITE  # B

                # scan 5-cell windows: A _ _ _ A
                for i in range(size - 4):
                    segment = line[i:i+5]
                    if segment[0] == target and segment[4] == target and segment[1] == EMPTY and segment[2] == EMPTY and segment[3] == EMPTY:
                        # fill the center (index +2)
                        old = line[i+2]
                        line[i+2] = opposite
                        if is_row:
                            debug_change("pattern_8", idx, i+2, old, opposite)
                        else:
                            debug_change("pattern_8", i+2, idx, old, opposite)
                        changed = True

            # write back to board
            if changed:
                if is_row:
                    board[idx] = line
                else:
                    for r in range(size):
                        board[r][idx] = line[r]

    return changed


'''
    Pattern 8: Remaining Color Flood
    When one color (A) has exactly 1 piece left to place in a row/column,
    and the opposite color (B) has multiple pieces remaining.

    If the number of EMPTY cells equals the remaining B pieces,
    then almost all EMPTY cells must be filled with B.

    However, we must still respect the "no three adjacent" rule.
    If placing B would create a triple, that cell must instead be A.

    This pattern effectively floods the remaining spaces with B,
    while only placing A where necessary to prevent illegal triples.

    Examples:

    Middle case:
        A _ B _ _ B A
        remaining B = number of EMPTY

        A B B A B B A

    Edge case:
        _ B _ _ B A
        remaining B = number of EMPTY

        B B A B B A
'''
def pattern_8(board):
    size = len(board)
    half = size // 2
    changed = False

    for is_row in [True, False]:
        for idx in range(size):

            line = board[idx] if is_row else [board[r][idx] for r in range(size)]

            count_white = line.count(WHITE)
            count_black = line.count(BLACK)

            white_left = half - count_white
            black_left = half - count_black

            if not ((white_left == 1 and black_left > 1) or (black_left == 1 and white_left > 1)):
                continue

            A = WHITE if white_left == 1 else BLACK
            B = BLACK if A == WHITE else WHITE
            B_left = black_left if A == WHITE else white_left

            empty_count = line.count(EMPTY)

            if empty_count != B_left:
                continue

            for i in range(size):
                if line[i] == EMPTY:

                    # test if B would create triple
                    left1 = line[i-1] if i-1 >= 0 else None
                    left2 = line[i-2] if i-2 >= 0 else None
                    right1 = line[i+1] if i+1 < size else None
                    right2 = line[i+2] if i+2 < size else None

                    illegal = (
                        (left1 == B and left2 == B) or
                        (right1 == B and right2 == B) or
                        (left1 == B and right1 == B)
                    )

                    new = A if illegal else B

                    old = line[i]
                    line[i] = new

                    if is_row:
                        debug_change("pattern_8", idx, i, old, new)
                    else:
                        debug_change("pattern_8", i, idx, old, new)

                    changed = True

            if is_row:
                board[idx] = line
            else:
                for r in range(size):
                    board[r][idx] = line[r]

    return changed