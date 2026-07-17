import copy

EMPTY = -1
WHITE = 0
BLACK = 1

class Constraint:   

    # DEBUGGING PURPOSE FUNCTION
    def color_name(value):
        if value == WHITE:
            return "WHITE"
        elif value == BLACK:
            return "BLACK"
        else:
            return "EMPTY"
        

    # DEBUG HELPER
    def debug_change(self, pattern, r, c, old, new):
        print(f"[{pattern}] row {r} col {c} changed {self.color_name(old)} -> {self.color_name(new)}")


    # GUARD
    def can_assign(self, board, r, c, value):
        rows = len(board)
        cols = len(board[0])

        if board[r][c] != EMPTY:
            return False

        row_half = cols // 2
        col_half = rows // 2

        # SIMULATE ASSIGN
        temp_board = copy.deepcopy(board)
        temp_board[r][c] = value

        # CHECK ROWS
        for rr in range(rows):
            row = temp_board[rr]

            Black = row.count(BLACK)
            white = row.count(WHITE)

            # max limit
            if Black > row_half or white > row_half:
                return False

            # no triple
            for i in range(cols - 2):
                if row[i] == row[i+1] == row[i+2] != EMPTY:
                    return False

        # CHECK COLS
        for cc in range(cols):
            col = [temp_board[i][cc] for i in range(rows)]

            Black = col.count(BLACK)
            white = col.count(WHITE)

            # max limit
            if Black > col_half or white > col_half:
                return False

            # no triple
            for i in range(rows - 2):
                if col[i] == col[i+1] == col[i+2] != EMPTY:
                    return False

        # DUPLICATE ROW CHECK (ONLY FULL ROWS)
        completed_rows = []

        for rr in range(rows):
            row = temp_board[rr]

            if EMPTY in row:
                continue

            if row in completed_rows:
                return False

            completed_rows.append(row[:])

        # DUPLICATE COL CHECK (ONLY FULL COLS)
        completed_cols = []

        for cc in range(cols):
            col = [temp_board[i][cc] for i in range(rows)]

            if EMPTY in col:
                continue

            if col in completed_cols:
                return False

            completed_cols.append(col[:])

        return True


    def safe_assign(self, board, r, c, value, pattern):
        if self.can_assign(board, r, c, value):
            old = board[r][c]
            board[r][c] = value
            # debug_change(pattern, r, c, old, value)
            return True
        return False


    # PATTERNS
    '''
        Apply constraint patterns to the puzzle board.
        @param board: 2D list of integers (-1 = empty, 0 = white, 1 = black)
        @return: Updated board after applying all possible rules
    '''
    def apply_constraints(self, board, difficulty=""):
        if difficulty != "special":
            patterns = [
                        self.pattern_1, 
                        self.pattern_2a, 
                        self.pattern_2b, 
                        self.pattern_3
                       ]
        else:
            patterns = [
                        self.pattern_2a, 
                        self.pattern_2b,
                        self.pattern_3
                       ]

        if difficulty in ["hard", "special"]:
            patterns += [
                         self.pattern_4, 
                         self.pattern_5, 
                         self.pattern_6, 
                         self.pattern_7, 
                         self.pattern_8
                        ]

        changed = True

        while changed:
            changed = False

            # apply rules
            # changed |= self.pattern_1(board)
            # changed |= self.pattern_2a(board)
            # changed |= self.pattern_2b(board)

            # if difficulty in ["hard", None]:
            #     changed |= self.pattern_3(board)
            #     changed |= self.pattern_4(board)
            #     changed |= self.pattern_5(board)
            #     changed |= self.pattern_6(board)
            #     changed |= self.pattern_7(board)
            #     changed |= self.pattern_8(board)

            for pattern in patterns:
                if pattern(board):
                    changed = True
                    break  # restart from pattern_1
            # changed = True
        return board


    # random fills
    '''
        Fill all empty cells with random colors (0 or 1).
        Used when no more deterministic constraints apply.
    '''
    def fill_random(board):
        import random

        rows = len(board)
        cols = len(board[0])

        for r in range(rows):
            for c in range(cols):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = random.choice([WHITE, BLACK])
                    # debug_change("fill_random", r, c, old, board[r][c])

        return board


    # deterministic patterns
    '''
        Pattern 1: Color Balancing
        Each row and column must contain an equal number of black and white tiles. Automatically fill the rest when one color reaches half of the row/column.
    '''
    def pattern_1(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        # CHECK ROWS
        for r in range(rows):
            row = board[r]
            half = cols // 2

            if row.count(WHITE) == half:
                for c in range(cols):
                    if row[c] == EMPTY:
                        changed |= self.safe_assign(board, r, c, BLACK, "pattern_1")

            elif row.count(BLACK) == half:
                for c in range(cols):
                    if row[c] == EMPTY:
                        changed |= self.safe_assign(board, r, c, WHITE, "pattern_1")
        
        # CHECK COLUMNS
        for c in range(cols):
            col = [board[r][c] for r in range(rows)]

            if col.count(WHITE) == half:
                for r in range(rows):
                    if board[r][c] == EMPTY:
                        changed |= self.safe_assign(board, r, c, BLACK, "pattern_1")

            elif col.count(BLACK) == half:
                for r in range(rows):
                    if board[r][c] == EMPTY:
                        changed |= self.safe_assign(board, r, c, WHITE, "pattern_1")

        return changed


    '''
        Pattern 2a: Three Adjacent
        - No three consecutive cells can have the same color.
        - Close open ends of two consecutive identical tiles.

        Example:
        _ 0 0 _  ->  1 0 0 1
    '''
    def pattern_2a(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        # CHECK ROWS
        for r in range(rows):
            for c in range(cols-2):
                triple = board[r][c:c+3]

                # If two same colors followed by an empty cell
                if triple[0] == triple[1] != EMPTY and triple[2] == EMPTY:
                    val = WHITE if triple[0] == BLACK else BLACK
                    changed |= self.safe_assign(board, r, c+2, val, "pattern_2a")

                # If two same colors preceded by an empty cell
                if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                    val = WHITE if triple[1] == BLACK else BLACK
                    changed |= self.safe_assign(board, r, c, val, "pattern_2a")

        # CHECK COLUMNS
        for c in range(cols):
            for r in range(rows - 2):
                triple = [board[r+i][c] for i in range(3)]

                if triple[0] == triple[1] != EMPTY and triple[2] == EMPTY:
                    val = WHITE if triple[0] == BLACK else BLACK
                    changed |= self.safe_assign(board, r+2, c, val, "pattern_2a")

                if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                    val = WHITE if triple[1] == BLACK else BLACK
                    changed |= self.safe_assign(board, r, c, val, "pattern_2a")

        return changed


    '''
        Pattern 2b: Three Adjacent
        - No three cells with the same color, even with one gap.
        - If two identical tiles are separated by one empty cell, fill the middle with the opposite color.

        Example:
        0 _ 0  ->  0 1 0
    '''
    def pattern_2b(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        # CHECK ROWS
        for r in range(rows):
            for c in range(cols - 2):
                triple = board[r][c:c+3]
                if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                    val = WHITE if triple[0] == BLACK else BLACK
                    changed |= self.safe_assign(board, r, c+1, val, "pattern_2b")

        # CHECK COLUMNS
        for c in range(cols):
            for r in range(rows - 2):
                triple = [board[r+i][c] for i in range(3)]
                if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                    val = WHITE if triple[0] == BLACK else BLACK
                    changed |= self.safe_assign(board, r+1, c, val, "pattern_2b")

        return changed


    '''
        Pattern 3: Uniqueness
        - Each row and column must be unique.
        - No two rows or columns can be identical.
    '''
    def pattern_3(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        # CHECK ROWS
        for r in range(rows):
            row = board[r]

            # ONLY if exactly 2 EMPTY
            if row.count(EMPTY) != 2:
                continue

            for ref_r in range(rows):
                if ref_r == r:
                    continue

                ref_row = board[ref_r]

                # reference must be FULL
                if EMPTY in ref_row:
                    continue

                # check if all FILLED cells match
                identical = True

                for c in range(cols):
                    if row[c] != EMPTY and row[c] != ref_row[c]:
                        identical = False
                        break

                if not identical:
                    continue

                # fill EMPTY with opposite
                for c in range(cols):
                    if row[c] == EMPTY:
                        val = WHITE if ref_row[c] == BLACK else BLACK

                        changed |= self.safe_assign(board, r, c, val, "pattern_3")

        # CHECK COLUMNS
        for c in range(cols):
            col = [board[r][c] for r in range(rows)]

            # ONLY if exactly 2 EMPTY
            if col.count(EMPTY) != 2:
                continue

            for ref_c in range(cols):
                if ref_c == c:
                    continue

                ref_col = [board[r][ref_c] for r in range(rows)]

                # reference must be FULL
                if EMPTY in ref_col:
                    continue

                # check if all FILLED cells match
                identical = True

                for r in range(rows):
                    if board[r][c] != EMPTY and board[r][c] != ref_col[r]:
                        identical = False
                        break

                if not identical:
                    continue

                # fill EMPTY with opposite
                for r in range(rows):
                    if board[r][c] == EMPTY:
                        val = WHITE if ref_col[r] == BLACK else BLACK

                        changed |= self.safe_assign(board, r, c, val, "pattern_3")

        return changed


    '''
        Pattern 4: Absolute One
        check if one color has only 1 piece left, then fill the rest with the opposite color

        1 _ _ 1 _ 0 1 1 0 1 1 0 (1 _ 0 _ 1) _ _ 1 
        1 0 0 1 0 0 1 1 0 1 1 0 (1 _ 0 _ 1) 0 0 1
    '''
    def pattern_4(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        # CHECK ROWS
        for r in range(rows):
            row = board[r]
            half = cols // 2

            count_white = row.count(WHITE)
            count_black = row.count(BLACK)
            empty_count = row.count(EMPTY)

            # check both colors left
            white_left = half - count_white
            Black_left = half - count_black

            # skip if both left with more or less than 1
            if white_left != 1 and Black_left != 1:
                continue

            for c in range(cols - 4):
                seg = row[c:c+5]

                # case: 1 _ 0 _ 1
                if seg[0] == seg[4] == BLACK and seg[2] == WHITE and seg[1] == seg[3] == EMPTY:
                    if Black_left == 1:  # only if BLACK left with 1 piece
                        for i in range(cols):
                            if i not in [c+1, c+3] and row[i] == EMPTY:
                                changed |= self.safe_assign(board, r, i, WHITE, "pattern_4")

                # case: 0 _ 1 _ 0
                elif seg[0] == seg[4] == WHITE and seg[2] == BLACK and seg[1] == seg[3] == EMPTY:
                    if white_left == 1:  # only if WHITE left with 1 piece
                        for i in range(cols):
                            if i not in [c+1, c+3] and row[i] == EMPTY:
                                changed |= self.safe_assign(board, r, i, BLACK, "pattern_4")

        # CHECK COLUMNS
        for c in range(cols):
            col = [board[r][c] for r in range(rows)]
            half = rows // 2

            count_white = col.count(WHITE)
            count_black = col.count(BLACK)
            empty_count = col.count(EMPTY)

            white_left = half - count_white
            Black_left = half - count_black

            if white_left != 1 and Black_left != 1:
                continue

            for r in range(rows - 4):
                seg = col[r:r+5]

                # case: 1 _ 0 _ 1
                if seg[0] == seg[4] == BLACK and seg[2] == WHITE and seg[1] == seg[3] == EMPTY:
                    if Black_left == 1:
                        # fill all empty cell unless idx in pattern
                        for i in range(rows):
                            if i not in [r+1, r+3] and col[i] == EMPTY:
                                changed |= self.safe_assign(board, i, c, WHITE, "pattern_4")

                # case: 0 _ 1 _ 0
                elif seg[0] == seg[4] == WHITE and seg[2] == BLACK and seg[1] == seg[3] == EMPTY:
                    if white_left == 1:
                        for i in range(rows):
                            if i not in [r+1, r+3] and col[i] == EMPTY:
                                changed |= self.safe_assign(board, i, c, BLACK, "pattern_4")
        
        return changed


    '''
        Pattern 5: A Third Balance Filling
        check if the remaining pieces have a 1:3 ratio

        find 4 adjacent EMPTY cells
        0 0 1 0 0 1 1 0 _ _ _ _ 0 1 1 0 0 1 1 0

        fill the edge cells with the color that has 3 pieces left
        0 0 1 0 0 1 1 0 1 _ _ 1 0 1 1 0 0 1 1 0
    '''
    def pattern_5(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        # CHECK ROWS
        for r in range(rows):
            row = board[r]
            half = cols // 2

            count_white = row.count(WHITE)
            count_black = row.count(BLACK)
            
            white_left = half - count_white
            Black_left = half - count_black

            # check ratio 1:3
            if sorted([white_left, Black_left]) == [1, 3]:
                color3 = BLACK if Black_left == 3 else WHITE

                # check if there are 4 EMPTY that adjacent
                for c in range(cols - 3):
                    if all(row[c+i] == EMPTY for i in range(4)):
                        # fill EDGE only
                        changed |= self.safe_assign(board, r, c, color3, "pattern_5")
                        changed |= self.safe_assign(board, r, c+3, color3, "pattern_5")

        # CHECK COLUMNS
        for c in range(cols):
            col = [board[r][c] for r in range(rows)]
            half = rows // 2

            count_white = col.count(WHITE)
            count_black = col.count(BLACK)

            white_left = half - count_white
            Black_left = half - count_black

            if sorted([white_left, Black_left]) == [1, 3]:
                color3 = BLACK if Black_left == 3 else WHITE

                for r in range(rows - 3):
                    if all(col[r+i] == EMPTY for i in range(4)):
                        changed |= self.safe_assign(board, r, c, color3, "pattern_5")
                        changed |= self.safe_assign(board, r+3, c, color3, "pattern_5")

        return changed


    '''
        Pattern 6: Forced Outside Fill
        If color X has exactly 1 tile left to place in a row/column
        and we detect a segment: X _ _ _ X
        then:
            - DO NOT fill the inside yet
            - fill ALL remaining EMPTY cells OUTSIDE the segment with opposite color Y

        This ensures the gap will not accidentally be filled with Y later,
        preventing illegal configuration: X Y Y Y X
    '''
    def pattern_6(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        def outside_fill(idx_start, idx_end, X, fixed_idx, is_row):
            nonlocal changed
            Y = WHITE if X == BLACK else BLACK

            limit = cols if is_row else rows

            for i in range(limit):
                if not (idx_start <= i <= idx_end):

                    r = fixed_idx if is_row else i
                    c = i if is_row else fixed_idx

                    if board[r][c] == EMPTY:
                        changed |= self.safe_assign(board, r, c, Y, "pattern_6") 

        # CHECK ROWS
        for r in range(rows):
            row = board[r]
            half = cols // 2

            count_white = row.count(WHITE)
            count_black = row.count(BLACK)

            white_left = half - count_white
            Black_left = half - count_black

            if white_left == 1 or Black_left == 1:
                X = WHITE if white_left == 1 else BLACK

                for c in range(cols - 4):
                    seg = row[c:c + 5]
                    if seg[0] == X and seg[4] == X and seg[1] == seg[2] == seg[3] == EMPTY:
                        outside_fill(c, c+4, X, r, True)

        # CHECK COLUMNS
        for c in range(cols):
            col = [board[r][c] for r in range(rows)]
            half = rows // 2

            count_white = col.count(WHITE)
            count_black = col.count(BLACK)
            
            white_left = half - count_white
            Black_left = half - count_black

            if white_left == 1 or Black_left == 1:
                X = WHITE if white_left == 1 else BLACK

                for r in range(rows - 4):
                    seg = col[r:r + 5]
                    if seg[0] == X and seg[4] == X and seg[1] == seg[2] == seg[3] == EMPTY:
                        outside_fill(r, r+4, X, c, False)

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
    def pattern_7(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        # CHECK ROWS
        for r in range(rows):
            row = board[r]
            half = cols // 2

            # count remaining pieces
            white_left = half - row.count(WHITE)
            Black_left = half - row.count(BLACK)

            # only proceed if one color has exactly 1 left
            if (white_left == 1 and Black_left > 1) or (Black_left == 1 and white_left > 1):
                A = WHITE if white_left == 1 else BLACK
                B = BLACK if A == WHITE else WHITE

                # scan 5-cell windows: A _ _ _ A
                for c in range(cols - 4):
                    seg = row[c:c+5]
                    if seg[0] == seg[4] == A and seg[1] == seg[2] == seg[3] == EMPTY:
                        changed |= self.safe_assign(board, r, c+2, B, "pattern_7")

        # CHECK COLUMNS
        for c in range(cols):
            col = [board[r][c] for r in range(rows)]
            half = rows // 2

            # count remaining pieces
            white_left = half - col.count(WHITE)
            Black_left = half - col.count(BLACK)

            if (white_left == 1 and Black_left > 1) or (Black_left == 1 and white_left > 1):
                A = WHITE if white_left == 1 else BLACK
                B = BLACK if A == WHITE else WHITE

                for r in range(rows - 4):
                    seg = col[r:r+5]
                    if seg[0] == seg[4] == A and seg[1] == seg[2] == seg[3] == EMPTY:
                        changed |= self.safe_assign(board, r+2, c, B, "pattern_7")

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
    def pattern_8(self, board):
        rows = len(board)
        cols = len(board[0])
        changed = False

        # CHECK ROWS
        for r in range(rows):
            row = board[r]
            half = cols // 2

            white_left = half - row.count(WHITE)
            Black_left = half - row.count(BLACK)

            if not ((white_left == 1 and Black_left > 1) or (Black_left == 1 and white_left > 1)):
                continue

            A = WHITE if white_left == 1 else BLACK
            B = BLACK if A == WHITE else WHITE
            B_left = Black_left if A == WHITE else white_left

            if row.count(EMPTY) != B_left:
                continue

            for c in range(cols):
                if row[c] == EMPTY:
                    # test if B would create triple
                    left1 = row[c-1] if c-1 >= 0 else None
                    left2 = row[c-2] if c-2 >= 0 else None
                    right1 = row[c+1] if c+1 < cols else None
                    right2 = row[c+2] if c+2 < cols else None

                    illegal = ((left1 == B and left2 == B) or (right1 == B and right2 == B) or (left1 == B and right1 == B))

                    val = A if illegal else B
                    changed |= self.safe_assign(board, r, c, val, "pattern_8")

        # CHECK COLUMNS
        for c in range(cols):
            col = [board[r][c] for r in range(rows)]
            half = rows // 2

            white_left = half - col.count(WHITE)
            Black_left = half - col.count(BLACK)

            if not ((white_left == 1 and Black_left > 1) or (Black_left == 1 and white_left > 1)):
                continue

            A = WHITE if white_left == 1 else BLACK
            B = BLACK if A == WHITE else WHITE
            B_left = Black_left if A == WHITE else white_left

            if col.count(EMPTY) != B_left:
                continue

            for r in range(rows):
                if board[r][c] == EMPTY:
                    left1 = col[r-1] if r-1 >= 0 else None
                    left2 = col[r-2] if r-2 >= 0 else None
                    right1 = col[r+1] if r+1 < rows else None
                    right2 = col[r+2] if r+2 < rows else None

                    illegal = ((left1 == B and left2 == B) or (right1 == B and right2 == B) or (left1 == B and right1 == B))

                    val = A if illegal else B
                    changed |= self.safe_assign(board, r, c, val, "pattern_8")

        return changed