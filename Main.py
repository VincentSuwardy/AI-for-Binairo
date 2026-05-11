import sys
import time
from WebIteractor import WebIteractor, URL
from Constraint import apply_constraints, fill_random
from Validator import is_valid
from Heuristic import random_fill, fill_most_constrained_cell, heuristic_density_fill
from Genetic import run_genetic, fitness

EMPTY = -1
WHITE = 0
BLACK = 1

'''
    DEFINE PUZZLE CONFIG
    size: 6 | 8 | 10 | 14 | 20 | daily (24x24) | weekly (30x30) | monthly (30x40)
    diff: easy | hard | None (for daily/weekly/monthly)
'''
PUZZLE_SIZE = "daily"
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
    Expand the board to make it 40 x 40 by padding -1 [unused]
'''
# def pad_board(board, target_rows=40, target_cols=40, pad_value=-1):
#     rows = len(board)
#     cols = len(board[0])
#     new_board = [[pad_value for _ in range(target_cols)] for _ in range(target_rows)]
#     for r in range(rows):
#         for c in range(cols):
#             new_board[r][c] = board[r][c]
#     return new_board

'''
    trim the expanded tiles from the board [unused]
'''
# def trim_board(board, real_rows=40, real_cols=30):
#     trimmed = []
#     for r in range(real_rows):
#         row = []
#         for c in range(real_cols):
#             row.append(board[r][c])
#         trimmed.append(row)
#     return trimmed

'''
    debug print cells
'''
def debug_count(board, label=""):
    EMPTY = -1
    WHITE = 0
    BLACK = 1

    empty = 0
    white = 0
    black = 0

    for row in board:
        for cell in row:
            if cell == EMPTY:
                empty += 1
            elif cell == WHITE:
                white += 1
            elif cell == BLACK:
                black += 1

    print(f"=================================================================\n[{label}] EMPTY={empty} WHITE={white} BLACK={black}\n=================================================================")

    return empty

'''
    debug print color
'''
def color_name(value):
    if value == WHITE:
        return "WHITE"
    elif value == BLACK:
        return "BLACK"
    else:
        return "EMPTY"

'''
    Preprocess using anchor + flip strategy:
    - Pick one most constrained cell
    - Try a value
    - Explore with heuristic
    - If invalid in first move > revert and flip the anchor value
    - Do while heuristic result is still valid
'''
def preprocess_board(board, difficulty):
    import copy

    board_copy = copy.deepcopy(board)

    # print initial board stats
    debug_count(board_copy, "initial")

    # initial constraint
    board_copy = apply_constraints(board_copy, difficulty)
    empty_counter = debug_count(board_copy, "after constraint")

    last_valid_board = copy.deepcopy(board_copy)
    if (empty_counter == 0):
        print("[stop] board is fully filled")
        return last_valid_board, empty_counter

    step = 0

    while True and empty_counter > 0:
        step += 1
        print(f"[step] {step}")

        before_fill = copy.deepcopy(board_copy)

        changed, r, c = fill_most_constrained_cell(board_copy)
        # changed, r, c = heuristic_density_fill(board_copy)

        if not changed:
            # print("[info] no EMPTY left")
            empty_counter = debug_count(last_valid_board, "no more moves")
            return last_valid_board, empty_counter

        board_copy = apply_constraints(board_copy, difficulty)

        if not is_valid(board_copy):

            print("[invalid] step produced invalid board")

            # special rule: flip if failure happens on first move
            if step == 1:
                first_value = board_copy[r][c]
                print("[flip] retry first move with flipped value")

                board_copy = copy.deepcopy(before_fill)

                # flip the value manually
                flipped = WHITE if first_value == BLACK else BLACK
                board_copy[r][c] = flipped
                print(f"[flip] Row {r} col {c} changed EMPTY -> {color_name(flipped)}")

                # fill_most_constrained_cell(board_copy)
                board_copy = apply_constraints(board_copy, difficulty)

                if is_valid(board_copy):
                    last_valid_board = copy.deepcopy(board_copy)
                    continue

            break

        last_valid_board = copy.deepcopy(board_copy)
        empty_counter = debug_count(board_copy, f"step {step}")

    # debug_count(board_copy, f"step {step}")
    print("[stop] returning last valid board")
    return last_valid_board, empty_counter


'''
    
'''
def create_fixed_mask(board):
    return [[cell != EMPTY for cell in row] for row in board]


'''
    Main program for solving and submitting.

    Steps:
        1. Initialize the web interactor
        2. Retrieve a puzzle from the web
        3. Apply constraint-based rules solving rules
        4. Apply all constraint patterns
        5. Apply heuristic to make search tree smaller
        5. Apply genetic algorithm
        6. Save both the puzzle and its solution locally
        7. Input the solution back into the website
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
        difficulty = "hard"
    else:
        difficulty = PUZZLE_DIFF

    # retrieve puzzle from the web
    id, board = iterator.open_puzzle(size, difficulty)
    start_time = time.time()

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
    # if size == "monthly" :
    #     board = pad_board(board)

    fixed_mask = create_fixed_mask(board)
    # original_board = [row[:] for row in board]

    # solving stage
    # if (difficulty == "easy"):
    #     board = apply_constraints(board, difficulty)
    #     debug_count(board, "initial")
    # else:
    board = apply_constraints(board, difficulty)
        # board = fill_random(board)    # (optionally) randomly fill remaining empty cells
        # board = preprocess_board(board, difficulty, 3, 3)
    
    # board, empty_counter = preprocess_board(board, difficulty)
    # if (empty_counter > 0):
    #     board, board_fitness = run_genetic(board, fixed_mask, PUZZLE_DIFF)
    # else:
    board_fitness = fitness(board)

    # if size == "monthly" :
    #     board = trim_board(board)

    answer = Answer(board)
    
    end_time = time.time()
    elapsed = end_time - start_time

    # debug fitness
    print(f"\nFinal fitness: {board_fitness:.2f}")

    # debug timer
    print("\n================ TIME STATS ================")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Total time: {elapsed/60:.2f} minutes")
    print("============================================\n")

    iterator.save_answer(id, answer, size, difficulty, elapsed, board_fitness)  # save the final solved answer to local file

    # input the solved answer into the website
    iterator.input_answer(answer)

    # (optional) close the browser session
    # iterator.close()

if __name__ == "__main__":
    main()