import os
import time
from collections import defaultdict

from Main import create_fixed_mask
from Genetic import Genetic
from Constraint import Constraint
from Heuristic import Heuristic

# PILIH MODE

# MODE = "5.3.1"        # preprocessing
# MODE = "5.3.2.1"      # preprocessing + heuristic 1
# MODE = "5.3.2.2"      # preprocessing + heuristic 2
# MODE = "5.3.2.3"      # preprocessing + heuristic 3
# MODE = "5.3.3.1"      # preprocessing + GA param kecil
# MODE = "5.3.3.2"      # preprocessing + GA param besar
# MODE = "5.3.3.3"      # preprocessing + GA param tuning
# MODE = "5.3.4.1"      # preprocessing + GA weight tetap
# MODE = "5.3.4.2"      # preprocessing + GA weight tuning
# MODE = "5.3.5"        # preprocessing + heuristic + GA

MODES = [
    "5.3.1",
    "5.3.2.1",
    "5.3.2.2",
    "5.3.2.3",
    "5.3.3.1",
    "5.3.3.2",
    "5.3.3.3",
    "5.3.4.1",
    "5.3.4.2",
    "5.3.5",
]

def run_all_modes(data_root="Data"):
    for mode in MODES:
        # reset stats tiap mode
        stats_by_category.clear()

        print("\n" + "="*60)
        print(f"RUNNING MODE : {mode}")
        print("="*60 + "\n")

        run_dataset(data_root, mode)


# GA PARAMETER
POPULATION_SIZE = 350
MAX_GENERATIONS = 800
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.80
ELITE_SIZE = 35
ADAPTIVE = [False, False]       # [Param, Weight]

stats_by_category = defaultdict(lambda: {
    "total": 0,
    "success": 0,
    "fail": 0
})


# HEURISTIC
def run_single_heuristic(board, difficulty, heuristic_fn, time_limit=60):
    start_time = time.time()

    while True:
        # stop karena waktu habis
        if time.time() - start_time >= time_limit:
            break

        # cek fitness dulu (kalau sudah selesai, langsung stop)
        if Genetic.fitness(board) == 0:
            break

        changed, _, _ = heuristic_fn(board)

        # kalau tidak ada perubahan, berhenti
        if not changed:
            break

        board = Constraint.apply_constraints(board, difficulty)

        # cek lagi setelah update
        if Genetic.fitness(board) == 0:
            break

    return board


# PARSE FILE
def parse_puzzle_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]

    puzzle_id = None
    size = None
    difficulty = None

    # FORMAT SPESIAL
    if lines[0].startswith("ID") and lines[1].startswith("Diff"):
        puzzle_id = lines[0].split(":")[1].strip()
        difficulty = lines[1].split(":")[1].strip().lower()

        board = []

        for line in lines[2:]:
            if not line.strip():
                continue

            board.append([int(x) for x in line.split()])

        rows = len(board)
        cols = len(board[0])

        # tentukan size berdasarkan tipe puzzle
        if difficulty == "daily":
            size = "24x24"
        elif difficulty == "weekly":
            size = "30x30"
        elif difficulty == "monthly":
            size = "30x40"
        else:
            size = f"{rows}x{cols}"

        return puzzle_id, size, difficulty, board

    # FORMAT
    puzzle_id = lines[0].split(":")[1].strip()
    size = lines[1].split(":")[1].strip()
    difficulty = lines[2].split(":")[1].strip()

    board = []

    for line in lines[4:]:
        if not line.strip():
            continue

        board.append([int(x) for x in line.split()])

    return puzzle_id, size, difficulty, board


# CATEGORY KEY
def get_category(size, difficulty):
    return f"{size}_{difficulty}"


# SAVE ANSWER
def save_answer(output_path, puzzle_id, size, difficulty, board, elapsed, board_fitness, weights, mode):
    w1, w2, w3 = weights

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"ID\t\t: {puzzle_id}\n")
        f.write(f"Size\t: {size}\n")
        f.write(f"Diff\t: {difficulty}\n")
        f.write("\n")

        f.write("---- Parameter ----\n")
        f.write(f"Population size\t: {POPULATION_SIZE}\n")
        f.write(f"Max generations\t: {MAX_GENERATIONS}\n")
        f.write(f"Mutation rate\t: {MUTATION_RATE}\n")
        f.write(f"Crossover rate\t: {CROSSOVER_RATE}\n")
        f.write(f"Elite size\t: {ELITE_SIZE}\n\n")

        f.write("---- Weights ----\n")

        f.write(f"w1\t: {w1}\n")
        f.write(f"w2\t: {w2}\n")
        f.write(f"w3\t: {w3}\n\n")

        for row in board:
            f.write(" ".join(f"{x:2d}" for x in row))
            f.write("\n")

        f.write("\n")
        f.write(f"Fitness : {board_fitness:.4f}\n")
        f.write(f"Time    : {elapsed:.4f} sec\n")


# SOLVE FILE
def solve_file(txt_file, mode):
    constraint = Constraint()
    genetic = Genetic()
    heuristic = Heuristic()

    print("=" * 60)
    print("Processing :", txt_file)

    puzzle_id, size, difficulty, board = (parse_puzzle_file(txt_file))
    category = get_category(size, difficulty)

    stats_by_category[category]["total"] += 1

    weights = (0, 0, 0)
    start_time = time.time()
    fixed_mask = create_fixed_mask(board)


    # 5.3.1
    # PREPROCESS
    if mode == "5.3.1":
        board = constraint.apply_constraints(board, difficulty)
        board_fitness = genetic.fitness(board)


    # 5.3.2.1
    # PREPROCESS + HEURISTIC 1
    elif mode == "5.3.2.1":
        board = constraint.apply_constraints(board, difficulty)
        board = run_single_heuristic(board, difficulty, heuristic.fill_most_constrained_cell)
        board_fitness = genetic.fitness(board)


    # 5.3.2.2
    # PREPROCESS + HEURISTIC 2
    elif mode == "5.3.2.2":
        board = constraint.apply_constraints(board, difficulty)
        board = run_single_heuristic(board, difficulty, heuristic.heuristic_density_fill)
        board_fitness = genetic.fitness(board)


    # 5.3.2.3
    # PREPROCESS + HEURISTIC 3
    elif mode == "5.3.2.3":
        board = constraint.apply_constraints(board, difficulty)
        board = run_single_heuristic(board, difficulty, heuristic.heuristic_line_fill)
        board_fitness = genetic.fitness(board)


    # 5.3.3.1
    # PREPROCESS + GA PARAM KECIL
    elif mode == "5.3.3.1":
        board = constraint.apply_constraints(board, difficulty)
        genetic.set_ga_params(population_size=150, max_generations=400,mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE, elite_size=15, adaptive=ADAPTIVE)

        if (genetic.fitness(board) < 0):
            board, board_fitness, weights = genetic.run_genetic(board, fixed_mask, difficulty)
        else:
            board_fitness = genetic.fitness(board);


    # 5.3.3.2
    # PREPROCESS + GA PARAM BESAR
    elif mode == "5.3.3.2":
        board = constraint.apply_constraints(board, difficulty)
        genetic.set_ga_params(population_size=300, max_generations=800,mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE, elite_size=30, adaptive=ADAPTIVE)

        if (genetic.fitness(board) < 0):
            board, board_fitness, weights = genetic.run_genetic(board, fixed_mask, difficulty)
        else:
            board_fitness = genetic.fitness(board);

    # 5.3.3.3
    # PREPROCESS + GA PARAM TUNING
    elif mode == "5.3.3.3":
        board = constraint.apply_constraints(board, difficulty)
        genetic.set_ga_params(population_size=POPULATION_SIZE, max_generations=MAX_GENERATIONS, mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE, elite_size=ELITE_SIZE, adaptive=[True, False])

        if (genetic.fitness(board) < 0):
            board, board_fitness, weights = genetic.run_genetic(board, fixed_mask, difficulty)
        else:
            board_fitness = genetic.fitness(board);


    # 5.3.4.1
    # PREPROCESS + GA WEIGHT TETAP
    elif mode == "5.3.4.1":
        board = constraint.apply_constraints(board, difficulty)
        genetic.set_ga_params(population_size=POPULATION_SIZE, max_generations=MAX_GENERATIONS, mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE, elite_size=ELITE_SIZE, adaptive=ADAPTIVE)

        if (genetic.fitness(board) < 0):
            board, board_fitness, weights = genetic.run_genetic(board, fixed_mask, difficulty)
        else:
            board_fitness = genetic.fitness(board);
    
    # 5.3.4.2
    # PREPROCESS + GA WEIGHT TUNING
    elif mode == "5.3.4.1":
        board = constraint.apply_constraints(board, difficulty)
        genetic.set_ga_params(population_size=POPULATION_SIZE, max_generations=MAX_GENERATIONS, mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE, elite_size=ELITE_SIZE, adaptive=[False, True])

        if (genetic.fitness(board) < 0):
            board, board_fitness, weights = genetic.run_genetic(board, fixed_mask, difficulty)
        else:
            board_fitness = genetic.fitness(board);
    
    # 5.3.2.2
    # PREPROCESS + (BEST) HEURISTIC + GA (BEST, BEST)
    elif mode == "5.3.2.2":
        board = constraint.apply_constraints(board, difficulty)
        board = run_single_heuristic(board, difficulty, heuristic.heuristic_line_fill)

        genetic.set_ga_params(population_size=POPULATION_SIZE, max_generations=MAX_GENERATIONS, mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE, elite_size=ELITE_SIZE, adaptive=[True, True])

        if (genetic.fitness(board) < 0):
            board, board_fitness, weights = genetic.run_genetic(board, fixed_mask, difficulty)
        else:
            board_fitness = genetic.fitness(board);

    else:
        raise Exception(
            f"MODE {mode} tidak dikenali"
        )

    elapsed = time.time() - start_time


    # STATS
    if board_fitness == 0:
        stats_by_category[category]["success"] += 1
    else:
        stats_by_category[category]["fail"] += 1

    folder_name = os.path.basename(os.path.dirname(txt_file))
    file_name = os.path.basename(txt_file)
    output_file = os.path.join("Answer", mode, folder_name, file_name)

    save_answer(output_file, puzzle_id, size, difficulty, board, elapsed, board_fitness, weights, mode)

    print(f"[DONE] Saved -> {output_file}")
    print(f"Fitness = {board_fitness:.4f}")
    print(f"Time = {elapsed:.2f} sec")



# RUN DATASET
def run_dataset(data_root="Data", mode=None):
    for root, _, files in os.walk(data_root):
        txt_files = sorted([f for f in files if f.endswith(".txt")])

        for file in txt_files:
            solve_file(os.path.join(root, file), mode)

    save_result(mode)


def parse_category(cat):
    size, diff = cat.split("_")
    return int(size), diff


def save_result(mode):
    base = os.path.join("Answer", mode)
    os.makedirs(base, exist_ok=True)

    with open(os.path.join(base, "result.txt"), "w", encoding="utf-8") as f:
        f.write(f"MODE: {mode}\n\n")
        grand_total = grand_success = grand_fail = 0

        for cat in sorted(
            stats_by_category.keys(),
            key=lambda x: (
                int(x.split("_")[0].split("x")[0]),
                int(x.split("_")[0].split("x")[1]),
                x.split("_")[1]
            )
        ):
            v = stats_by_category[cat]

            total = v["total"]
            success = v["success"]
            fail = v["fail"]

            rate = (success / total * 100) if total else 0

            f.write(f"[{cat}]\n")
            f.write(f"Total   : {total}\n")
            f.write(f"Success : {success}\n")
            f.write(f"Fail    : {fail}\n")
            f.write(f"Rate    : {rate:.2f}%\n\n")

            grand_total += total
            grand_success += success
            grand_fail += fail

        f.write("==== OVERALL ====\n")
        f.write(f"Total   : {grand_total}\n")
        f.write(f"Success : {grand_success}\n")
        f.write(f"Fail    : {grand_fail}\n")
        f.write(f"Rate    : {(grand_success/grand_total*100 if grand_total else 0):.2f}%\n")


# ENTRY
if __name__ == "__main__":
    # run_dataset("Data")
    run_all_modes("Data")