import sys
from WebIteractor import WebIteractor, URL
from Constraint import apply_constraints, fill_random
from Validator import is_valid
from Heuristic import random_fill

'''
    DEFINE PUZZLE CONFIG
    size: 6 | 8 | 10 | 14 | 20 | daily | weekly | monthly
    diff: easy | hard | None (for daily/weekly/monthly)
'''
PUZZLE_SIZE = "10"
PUZZLE_DIFF = "hard"

'''
    Represent the final solved answer of a puzzle.
    Constains an internal State class that stores the current board configuration as a 2D list of integers.
'''
class Answer:
    class State:
        def __init__(self, board):
            # store the solved board (2D array)
            self.board = board
    def __init__(self, board):
        self.state = self.State(board)

# Method for processing monthly board, since monthly board is a 30 x 40 board.
'''
    Expand the board to make it 40 x 40 by padding -1
'''
def pad_board(board, target_rows=40, target_cols=40, pad_value=-1):
    rows = len(board)
    cols = len(board[0])
    new_board = [[pad_value for _ in range(target_cols)] for _ in range(target_rows)]
    for r in range(rows):
        for c in range(cols):
            new_board[r][c] = board[r][c]
    return new_board

'''
    trim the expanded tiles from the board
'''
def trim_board(board, real_rows=40, real_cols=30):
    trimmed = []
    for r in range(real_rows):
        row = []
        for c in range(real_cols):
            row.append(board[r][c])
        trimmed.append(row)
    return trimmed

'''
    Preprocess using anchor + flip strategy:
    - Pick one anchor cell
    - Try a value
    - Explore with random fills
    - If invalid → revert and flip the anchor value
'''
def preprocess_board(board, difficulty, max_steps=1, max_retry=3):
    import copy
    import random

    for attempt_idx in range(max_retry):
        print(f"[retry] attempt {attempt_idx + 1}")
        base_board = copy.deepcopy(board)

        # Step 1: apply constraints first
        base_board = apply_constraints(base_board, difficulty)

        # Find EMPTY cells
        size = len(base_board)
        empty_cells = [
            (r, c)
            for r in range(size)
            for c in range(size)
            if base_board[r][c] == -1
        ]

        if not empty_cells:
            print("[retry] no EMPTY left, returning")
            return base_board

        # === PICK ANCHOR ===
        r, c = random.choice(empty_cells)

        # Try both values: first random, then flipped
        first_value = random.choice([0, 1])
        attempts = [first_value, 1 - first_value]

        for val in attempts:
            board_copy = copy.deepcopy(base_board)

            # Apply anchor
            board_copy[r][c] = val

            # Apply constraint after anchor
            # board_copy = apply_constraints(board_copy, difficulty)
            new_board = apply_constraints(board_copy, difficulty)

            if not is_valid(new_board):
                print("[anchor] invalid, trying next value")
                continue

            board_copy = new_board

            # === EXPLORE ===
            for step in range(max_steps):
                print(f"[explore] step {step + 1}")

                changed = random_fill(board_copy)
                if not changed:
                    break

                board_copy = apply_constraints(board_copy, difficulty)

            # === VALIDATE ===
            if is_valid(board_copy):
                print("[validate] SUCCESS - board is valid")
                return board_copy
            else:
                print("[validate] FAILED - board is invalid")

    # kalau dua-duanya gagal → retry outer loop
    print("[fail] returning original board")
    board = apply_constraints(board, difficulty)
    return board  # fallback

'''
    Main program for solving and submitting.

    Steps:
        1. Initialize the web interactor.
        2. Retrieve a puzzle from the web.
        3. Apply constraint-based rules solving rules.
        4. Apply all constraint patterns.
        5. TODO: Apply genetic algorithm based on selected reference(s).
        6. Save both the puzzle and its solution locally.
        7. Input the solution back into the website.
'''
def main():
    # error handler
    if PUZZLE_SIZE not in ["6", "8", "10", "14", "20", "daily", "weekly", "monthly"]:
        sys.exit("[ERROR] Invalid puzzle size!")
    if PUZZLE_SIZE not in ["daily", "weekly", "monthly"] and PUZZLE_DIFF not in ["easy", "hard"]:
        sys.exit("[ERROR] Invalid puzzle difficulty!")

    # initialize the web iterator
    iterator = WebIteractor(URL)

    # define puzzle config
    size = PUZZLE_SIZE
    if PUZZLE_SIZE in ["daily", "weekly", "monthly"]:
        difficulty = None
    else:
        difficulty = PUZZLE_DIFF

    # retrieve puzzle from the web
    id, board = iterator.open_puzzle(size, difficulty)

    # validate if puzzle was successfully retrieved
    if not board:
        print("Fail to get puzzle")
        iterator.close()
        return
    
    # debug: puzzle information
    # print(f"Succesfully get puzzle")
    # print("Board:")
    # for row in board:
    #     print(" ".join(str(x) for x in row))

    # save original puzzle locally
    iterator.save_puzzle(id, board, size, difficulty)
    if size == "monthly" :
        board = pad_board(board)

    # solving stage
    # board = apply_constraints(board, PUZZLE_DIFF)
    # board = fill_random(board)    # (optionally) randomly fill remaining empty cells
    board = preprocess_board(board, difficulty, 3, 3)

    if size == "monthly" :
        board = trim_board(board)

    answer = Answer(board)
    iterator.save_answer(id, answer, size, difficulty)  # save the final solved answer to local file

    # input the solved answer into the website
    iterator.input_answer(answer)

    # (optional) close the browser session
    # iterator.close()

if __name__ == "__main__":
    main()