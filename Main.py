import time

from WebInteractor import WebInteractor, URL
from Constraint import Constraint
from Validator import Validator
from Heuristic import Heuristic
from Genetic import Genetic

EMPTY = -1
WHITE = 0
BLACK = 1

# DEFAULT PUZZLE CONFIG
'''
    DEFINE PUZZLE CONFIG
    size: 6 | 8 | 10 | 14 | 20 | daily (24x24) | weekly (30x30) | monthly (30x40)
    diff: easy | hard | None (for daily/weekly/monthly)
'''
PUZZLE_SIZE = "20"
PUZZLE_DIFF = "hard"

# DEFAULT GPA CONFIG
GPA_CONFIG = {
    "population_size": 350,
    "max_generations": 800,
    "mutation_rate": 0.1,
    "crossover_rate": 0.8,
    "elite_size": 35,
    "adaptive": [False, False]      # [param, weight]
}

# Answer Class
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


# DEBUG
'''
    debug print cells
'''
def debug_count(board, label=""):
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
def preprocess_board(board, difficulty, timeout=60):
    import copy
    import random
    import time

    constraint = Constraint()
    heuristic = Heuristic()
    validator = Validator()

    start_time = time.time()

    best_board = None
    best_fitness = 999999
    best_empty = 999999

    restart = 0

    while time.time() - start_time < timeout:
        restart += 1
        print(f"\n================ RESTART {restart} ================")
        board_copy = copy.deepcopy(board)

        # INITIAL CONSTRAINT
        board_copy = constraint.apply_constraints(board_copy, difficulty)

        if not validator.is_globally_valid(board_copy):
            print("[invalid] initial board globally invalid")
            continue

        last_valid_board = copy.deepcopy(board_copy)
        empty_counter = debug_count(board_copy, "initial")
        step = 0

        if empty_counter == 0:
            return last_valid_board, 0

        # MAIN HEURISTIC LOOP
        while empty_counter > 0:
            step += 1
            before_fill = copy.deepcopy(board_copy)

            # RANDOMIZED HEURISTIC
            heuristic_choice = random.choice([
                heuristic.heuristic_line_fill,
                # heuristic.heuristic_density_fill,
                # heuristic.fill_most_constrained_cell
            ])
            changed, r, c = heuristic_choice(board_copy)

            # no more progress
            if not changed:
                print("[stop] no more heuristic moves")
                break

            # APPLY CONSTRAINTS
            board_copy = constraint.apply_constraints(board_copy, difficulty)

            # GLOBAL VALIDATION
            if not validator.is_globally_valid(board_copy):
                print(f"[rollback] invalid at step {step}")
                # rollback
                board_copy = before_fill
                break
 
            # UPDATE BEST STATE
            last_valid_board = copy.deepcopy(board_copy)

            empty_counter = debug_count(board_copy, f"restart {restart} step {step}")

            current_fitness = Genetic.fitness(board_copy)

            if (current_fitness < best_fitness or empty_counter < best_empty):
                best_board = copy.deepcopy(board_copy)
                best_fitness = current_fitness
                best_empty = empty_counter
                print(
                    f"[best] fitness={best_fitness:.2f} "
                    f"empty={best_empty}"
                )

            # PERFECT GLOBAL STATE
            if empty_counter == 0:
                if validator.is_globally_valid(board_copy):
                    print("[SUCCESS] globally solved board")
                    return board_copy, 0

        print("[restart] trying another heuristic path...")

    # TIMEOUT FALLBACK
    print("\n========================================")
    print("[timeout] preprocess timeout reached")
    print(f"[best fitness] {best_fitness}")
    print(f"[best empty] {best_empty}")
    print("========================================\n")

    return best_board, best_empty


'''
    Util to mark origin hint from board
'''
def create_fixed_mask(board):
    return [[cell != EMPTY for cell in row] for row in board]


# OPTION 1 - PLAY PUZZLE
def play_puzzle():
    print("\nSize: [6, 8, 10, 14, 20, daily, weekly, monthly]")
    size = input("> Puzzle size: ").strip().lower()

    valid_sizes = ["6", "8", "10", "14", "20", "daily", "weekly", "monthly"]
    if size not in valid_sizes:
        print("[ERROR] Invalid size")
        return
    
    if size in ["daily", "weekly", "monthly"]:
        difficulty = "special"
        print("Diff auto set to special")
    else:
        print("Diff: [easy, hard]")
        difficulty = input("> Puzzle diff: ").strip().lower()

        if difficulty not in ["easy", "hard", "special"]:
            print("[ERROR] Invalid difficulty")
            return

    interactor = WebInteractor(URL)
    puzzle_id, board = interactor.open_puzzle(size, difficulty)

    if not board:
        print("Fail to get puzzle")
        interactor.close()
        return

    start_time = time.time()

    interactor.save_puzzle(puzzle_id, board, size, difficulty)
    fixed_mask = create_fixed_mask(board)

    board, empty_counter = preprocess_board(board, difficulty)

    # GPA / GENETIC ALGORITHM
    genetic = Genetic()
    weights = None
    if empty_counter > 0:
        genetic.set_ga_params(
            population_size=GPA_CONFIG["population_size"],
            max_generations=GPA_CONFIG["max_generations"],
            mutation_rate=GPA_CONFIG["mutation_rate"],
            crossover_rate=GPA_CONFIG["crossover_rate"],
            elite_size=GPA_CONFIG["elite_size"],
            adaptive=GPA_CONFIG["adaptive"]
        )
        board, board_fitness, weights = genetic.run_genetic(
            board,
            fixed_mask,
            difficulty
        )

    board_fitness = Genetic.fitness(board)
    answer = Answer(board)

    elapsed = time.time() - start_time

    print(f"\nFinal fitness: {board_fitness:.2f}")
    print("\n================ TIME STATS ================")
    print(f"Total time: {elapsed:.2f} seconds")
    print(f"Total time: {elapsed/60:.2f} minutes")
    print("============================================\n")

    interactor.save_answer(puzzle_id, answer, size, difficulty, elapsed, board_fitness, GPA_CONFIG, weights)

    interactor.input_answer(answer)
    # interactor.close()


# OPTION 2 - COLLECT DATA
def collect_puzzle_data():
    print("\nSize: [6, 8, 10, 14, 20, daily, weekly, monthly]")
    size = input("> Puzzle size: ").strip().lower()

    valid_sizes = ["6", "8", "10", "14", "20", "daily", "weekly", "monthly"]
    if size not in valid_sizes:
        print("[ERROR] Invalid size")
        return

    if size in ["daily", "weekly", "monthly"]:
        difficulty = "hard"
    else:
        print("Diff: [easy, hard]")
        difficulty = input("> Puzzle diff: ").strip().lower()

        if difficulty not in ["easy", "hard"]:
            print("[ERROR] Invalid difficulty")
            return

    try:
        total_data = int(input("> Number of puzzles: "))
        if total_data <= 0:
            print("[ERROR] Number must be greater than 0")
            return
    except ValueError:
        print("[ERROR] Invalid number")
        return
    
    for i in range(total_data):
        interactor = WebInteractor(URL)
        print(f"\nTaking puzzle {i+1}/{total_data}...")

        puzzle_id, board = interactor.open_puzzle(size, difficulty)

        if not board:
            print("Fail to get puzzle")
            continue

        interactor.save_puzzle(
            puzzle_id,
            board,
            size,
            difficulty
        )

        interactor.close()
        print("> Puzzle saved")
    print("> All puzzle collected")


# OPTION 3 - CONFIG GPA
def configure_gpa():
    print()

    adaptive_param = input(f"> Adaptive param (default: {GPA_CONFIG['adaptive'][1]}) (T/F): ").strip()

    if not adaptive_param:
        population_size = input(f"> Population size (default: {GPA_CONFIG['population_size']}): ").strip()
        max_generations = input(f"> Max generations (default: {GPA_CONFIG['max_generations']}): ").strip()
        elite_size = input(f"> Elite size (default: 10% * population_size): ").strip()

    mutation_rate = input(f"> Mutation rate (default: {GPA_CONFIG['mutation_rate']}): ").strip()
    crossover_rate = input(f"> Crossover rate (default: {GPA_CONFIG['crossover_rate']}): ").strip()
    adaptive_weight = input(f"> Adaptive weight (default: {GPA_CONFIG['adaptive'][1]}) (T/F): ").strip()

    if adaptive_param == "T" or adaptive_param == "t":
        GPA_CONFIG["adaptive"][0] = True
    else:
        GPA_CONFIG["adaptive"][0] = False

    if adaptive_param == "F" or adaptive_param == "f":
        if population_size:
            GPA_CONFIG["population_size"] = int(population_size)

        if max_generations:
            GPA_CONFIG["max_generations"] = int(max_generations)

        if elite_size:
            GPA_CONFIG["elite_size"] = int(elite_size)
    else:
        GPA_CONFIG["population_size"] = -1
        GPA_CONFIG["max_generations"] = -1
        GPA_CONFIG["elite_size"] = -1

    if mutation_rate:
        GPA_CONFIG["mutation_rate"] = float(mutation_rate)

    if crossover_rate:
        GPA_CONFIG["crossover_rate"] = float(crossover_rate)

    if adaptive_weight == "T" or adaptive_weight == "t":
        GPA_CONFIG["adaptive"][1] = True
    else:
        GPA_CONFIG["adaptive"][1] = False

    print("\n[GPA CONFIG UPDATED] [-1 means parameter is adaptive]")
    print(GPA_CONFIG)


# MAIN MENU LOOP
def main_menu():
    while True:
        print("\nSelect options:")
        print("1. play puzzle using GPA")
        print("2. collect puzzle data")
        print("3. configure GPA")
        print('Type "exit" to quit')

        choice = input("> Select: ").strip().lower()

        if choice == "exit":
            print("Exiting...")
            break

        elif choice == "1":
            play_puzzle()

        elif choice == "2":
            collect_puzzle_data()

        elif choice == "3":
            configure_gpa()

        else:
            print("[ERROR] Invalid option")


# ENTRY
if __name__ == "__main__":
    main_menu()