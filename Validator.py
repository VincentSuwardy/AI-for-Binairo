EMPTY = -1
WHITE = 0
BLACK = 1

class Validator:
    '''
        Check if one line is locally valid.

        Rules:
        - no more than half of each color
        - no 3 consecutive identical colors
    '''
    def validate_line(self, line):
        size = len(line)
        half = size // 2

        if line.count(WHITE) > half:
            return False

        if line.count(BLACK) > half:
            return False

        for i in range(size - 2):

            a = line[i]
            b = line[i + 1]
            c = line[i + 2]

            if a == b == c != EMPTY:
                return False

        return True


    '''
        Generate all valid completions for one line.

        Used for future feasibility checking.
    '''
    def generate_line_possibilities(self, line):
        results = []
        size = len(line)

        def backtrack(index, current):
            # local pruning
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

            # try both colors
            for color in [WHITE, BLACK]:
                current[index] = color
                backtrack(index + 1, current)

            current[index] = EMPTY

        backtrack(0, line[:])
        return results


    '''
        Local validator.

        Rules:
        - no more than half color
        - no 3 consecutive
        - no duplicate full rows/cols
    '''
    def is_valid(self, board):
        rows = len(board)
        cols = len(board[0])

        # ROWS
        for r in range(rows):

            row = board[r]

            if not self.validate_line(row):
                return False

        # COLS
        for c in range(cols):

            col = [board[r][c] for r in range(rows)]

            if not self.validate_line(col):
                return False

        # UNIQUE ROWS
        full_rows = [
            tuple(board[r])
            for r in range(rows)
            if EMPTY not in board[r]
        ]

        if len(full_rows) != len(set(full_rows)):
            return False

        # UNIQUE COLS
        full_cols = []

        for c in range(cols):
            col = tuple(board[r][c] for r in range(rows))

            if EMPTY not in col:
                full_cols.append(col)

        if len(full_cols) != len(set(full_cols)):
            return False

        return True


    '''
        Check if a line still has at least one
        possible valid completion.

        This catches globally dead states early.
    '''
    def has_valid_completion(self, line):
        possibilities = self.generate_line_possibilities(line)

        return len(possibilities) > 0


    '''
        Future feasibility validator.

        Checks:
        - every row still solvable
        - every column still solvable
    '''
    def validate_future_feasibility(self, board):
        rows = len(board)
        cols = len(board[0])

        # ROWS
        for r in range(rows):
            row = board[r]

            if not self.has_valid_completion(row):
                return False

        # COLS
        for c in range(cols):
            col = [board[r][c] for r in range(rows)]

            if not self.has_valid_completion(col):
                return False

        return True


    '''
        Stronger partial duplicate validator.

        Prevents rows/cols from becoming
        impossible duplicate states.

        Example:
        W B _ _
        W B _ _

        dangerous because both rows may
        eventually become identical.
    '''
    def validate_partial_patterns(self, board):
        rows = len(board)
        cols = len(board[0])

        # ROW PATTERNS
        for r1 in range(rows):
            for r2 in range(r1 + 1, rows):
                row1 = board[r1]
                row2 = board[r2]

                compatible = True

                for a, b in zip(row1, row2):
                    # ignore EMPTY
                    if a == EMPTY or b == EMPTY:
                        continue

                    # conflict found
                    if a != b:
                        compatible = False
                        break

                # rows are currently compatible
                if compatible:
                    empty1 = row1.count(EMPTY)
                    empty2 = row2.count(EMPTY)

                    # dangerous near-duplicate
                    if empty1 == empty2 and empty1 <= 2:
                        return False

        # COLUMN PATTERNS

        for c1 in range(cols):
            for c2 in range(c1 + 1, cols):
                col1 = [board[r][c1] for r in range(rows)]
                col2 = [board[r][c2] for r in range(rows)]

                compatible = True

                for a, b in zip(col1, col2):
                    if a == EMPTY or b == EMPTY:
                        continue

                    if a != b:
                        compatible = False
                        break

                if compatible:
                    empty1 = col1.count(EMPTY)
                    empty2 = col2.count(EMPTY)

                    if empty1 == empty2 and empty1 <= 2:
                        return False
        return True


    '''
        GLOBAL VALIDATOR

        Stronger than local validation.

        Includes:
        - local rules
        - future feasibility
        - partial duplicate detection
    '''
    def is_globally_valid(self, board):
        # local rules first
        if not self.is_valid(board):
            return False

        # future solvability
        if not self.validate_future_feasibility(board):
            return False

        # anti-deadlock duplicate patterns
        if not self.validate_partial_patterns(board):
            return False

        return True