import random

EMPTY = -1
WHITE = 0
BLACK = 1

class Heuristic:

    # DEBUGGING PURPOSE FUNCTION
    def color_name(value):
        if value == WHITE:
            return "WHITE"
        elif value == BLACK:
            return "BLACK"
        else:
            return "EMPTY"

    # DEBUG HELPER
    def debug_change(self, heuristic, r, c, old, new):
        print(f"[{heuristic}] Row {r} col {c} changed {self.color_name(old)} -> {self.color_name(new)}")


    '''
        Fill one random EMPTY cell with a random color (WHITE or BLACK).
        Returns True if a cell was filled, False if no EMPTY cells remain.
    '''
    def random_fill(self, board):
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

        # debug_change("random_fill", r, c, old, new)

        return True, r, c

    '''
        1. select the most constrained cells (row or column with the least EMPTY cell(s))
        2. from selected cells, select the most constrained (column or row with the least EMPTY cell(s))
        3. fill the selected cell with random 0/1
    '''
    def fill_most_constrained_cell(self, board):
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

        # debug_change("fill_most_constrained_cell", r, c, old, new)

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

    def heuristic_density_fill(self, board, threshold=0.8, max_attempts=100):
        import random

        rows = len(board)
        cols = len(board[0])

        h, w = self.get_window_size(rows, cols)

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
                # debug_change("density_fill", r, c, old, new)

                return True, r, c

        # if there is no candidate
        return False, None, None

    def opposite(self, color):
        return BLACK if color == WHITE else WHITE


    '''
        Validate one line (row/column)

        Rules:
        1. no 3 consecutive same colors
        2. color count must not exceed half
    '''
    def validate_line(self, line):
        size = len(line)
        limit = size // 2

        # balance check
        if line.count(WHITE) > limit:
            return False

        if line.count(BLACK) > limit:
            return False

        # no triple color
        for i in range(size - 2):
            a, b, c = line[i], line[i + 1], line[i + 2]

            if a != EMPTY and a == b == c:
                return False

        return True


    '''
        Recursively generate all valid completions for one line.

        Example:
        [W, W, EMPTY]

        only valid result:
        [W, W, B]

        because WWW is forbidden.
    '''
    def generate_line_possibilities(self, line):
        results = []
        size = len(line)

        def backtrack(index, current):
            # pruning
            if not self.validate_line(current):
                return

            # finish
            if index == size:
                if EMPTY not in current:
                    results.append(current[:])
                return

            # fixed value
            if line[index] != EMPTY:
                current[index] = line[index]
                backtrack(index + 1, current)
                return

            # try WHITE / BLACK
            for color in [WHITE, BLACK]:
                current[index] = color
                backtrack(index + 1, current)

            current[index] = EMPTY

        backtrack(0, line[:])

        return results


    '''
        Select row/column with medium EMPTY count.

        Avoid:
        - too few EMPTY -> not much information
        - too many EMPTY -> search space too large
    '''
    def collect_candidate_lines(self, board, min_empty=2, max_empty=10):
        rows = len(board)
        cols = len(board[0])

        candidates = []

        # rows
        for r in range(rows):
            empty_count = board[r].count(EMPTY)

            if min_empty <= empty_count <= max_empty:
                candidates.append(("row", r, empty_count))

        # columns
        for c in range(cols):
            column = [board[r][c] for r in range(rows)]

            empty_count = column.count(EMPTY)

            if min_empty <= empty_count <= max_empty:
                candidates.append(("col", c, empty_count))

        # prioritize more constrained lines
        candidates.sort(key=lambda x: x[2])

        return candidates


    '''
        Main heuristic:
        1. choose candidate row/column
        2. generate all valid possibilities
        3. find forced cells
        4. fill guaranteed value
    '''
    def heuristic_line_fill(self, board, min_empty=2, max_empty=10):
        rows = len(board)
        cols = len(board[0])

        candidates = self.collect_candidate_lines(board, min_empty, max_empty)

        if not candidates:
            return False, None, None

        # kandidat sudah terurut berdasarkan jumlah EMPTY
        best_empty = candidates[0][2]

        # ambil semua kandidat dengan constraint terbaik
        best_candidates = [
            c for c in candidates
            if c[2] == best_empty
        ]

        # random urutan kandidat
        # random.shuffle(best_candidates)
        random.shuffle(candidates)

        for line_type, index, _ in candidates:

            # ambil line
            if line_type == "row":
                line = board[index][:]
            else:
                line = [board[r][index] for r in range(rows)]

            # generate semua kemungkinan valid
            possibilities = self.generate_line_possibilities(line)

            if not possibilities:
                continue

            forced_moves = []

            # cari semua forced cell
            for i in range(len(line)):
                if line[i] != EMPTY:
                    continue

                values = set(p[i] for p in possibilities)

                if len(values) == 1:
                    forced_moves.append((i, values.pop()))

            # jika ada forced move
            if forced_moves:
                i, value = random.choice(forced_moves)

                if line_type == "row":
                    old = board[index][i]
                    board[index][i] = value

                    # debug_change("heuristic_line_fill", index, i, old, value)

                    return True, index, i

                else:
                    old = board[i][index]
                    board[i][index] = value

                    # debug_change("heuristic_line_fill", i, index, old, value)

                    return True, i, index

        return False, None, None