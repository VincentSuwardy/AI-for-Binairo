import random
import copy

EMPTY = -1
WHITE = 0
BLACK = 1

'''
    Genetic Algorithm hyperparameters
'''
POPULATION_SIZE = 200
MAX_GENERATIONS = 800

MUTATION_RATE = 0.3
CROSSOVER_RATE = 0.8
ELITE_SIZE = 2


'''
    initialization population
    - fill the rest EMPTY cell(s) with random WHITE or BLACK
'''
def init_population(base_board, fixed_mask, pop_size):
    population = []

    for _ in range(pop_size):
        board = copy.deepcopy(base_board)

        for r in range(len(board)):
            for c in range(len(board[0])):
                if not fixed_mask[r][c]:
                    board[r][c] = random.choice([WHITE, BLACK])

        population.append(board)

    return population

'''
    count fitness function
    - for every triplets made,                penalty_1 += 1
    - count for balancing                     penalty_2 += |total_WHITE - total_BLACK|
    - for every duplicates row(s)/col(s),     penalty_3 += 1

    fitness = (w1 * penalty_1) + (w2 * penalty_2) + (w3 * penalty_3)

    where wn is weight for every penalty
'''
def fitness(board, w1=5, w2=2, w3=10):
    rows = len(board)
    cols = len(board[0])

    penalty_1 = 0
    penalty_2 = 0
    penalty_3 = 0

    # Penalty_1: triplets
    # check rows
    for r in range(rows):
        for c in range(cols - 2):
            if board[r][c] != -1:
                if board[r][c] == board[r][c+1] == board[r][c+2]:
                    penalty_1 += 1

    # check columns
    for c in range(cols):
        for r in range(rows - 2):
            if board[r][c] != -1:
                if board[r][c] == board[r+1][c] == board[r+2][c]:
                    penalty_1 += 1

    
    # Penalty_2 : balance
    # every rows
    for r in range(rows):
        whites = board[r].count(0)
        blacks = board[r].count(1)
        penalty_2 += abs(whites - blacks)

    # every columns
    for c in range(cols):
        col = [board[r][c] for r in range(rows)]
        whites = col.count(0)
        blacks = col.count(1)
        penalty_2 += abs(whites - blacks)


    # Penalty_3: duplicates
    # check rows
    seen_rows = []
    for r in range(rows):
        if -1 not in board[r]:
            if board[r] in seen_rows:
                penalty_3 += 1
            else:
                seen_rows.append(board[r])

    # check columns
    seen_cols = []
    for c in range(cols):
        col = [board[r][c] for r in range(rows)]
        if -1 not in col:
            if col in seen_cols:
                penalty_3 += 1
            else:
                seen_cols.append(col)

    
    # final fitness
    penalty = (w1 * penalty_1) + (w2 * penalty_2) + (w3 * penalty_3)

    return -penalty


'''
    Selection using Firefly Mating Algorithm
'''
def selection(population, num_pairs):
    pairs = []

    fitness_values = [fitness(idx) for idx in population]
    # total_fit = sum(fitness_values)

    for _ in range(num_pairs):
        i = random.randint(0, len(population)-1)
        parent1 = population[i]

        probs = []
        for j in range(len(population)):
            # if fitness_values[j] > fitness_values[i]:
            #     probs.append(fitness_values[j] - fitness_values[i])
            # else:
            #     probs.append(0)

            # attraction by fitness 
            diff = fitness_values[j] - fitness_values[i]
            probs.append(max(diff, 0))

        if sum(probs) > 0:
            parent2 = random.choices(population, weights=probs, k=1)[0]
        else:
            parent2 = random.choice(population)

        pairs.append((parent1, parent2))
    
    return pairs


'''
    Crossover
    - row based crossover: select random rows from 2 parents to make new child
    - col based crossover: select random cols from 2 parents to make new child
'''
def crossover(parent1, parent2, fixed_mask):
    if (random.random() > 0.5):
        return row_based_crossover(parent1, parent2, fixed_mask)
    else:
        return col_based_crossover(parent1, parent2, fixed_mask)

# row based crossover
def row_based_crossover(parent1, parent2, fixed_mask):
    rows = len(parent1)
    cols = len(parent1[0])

    child = [[-1 for _ in range(cols)] for _ in range(rows)]
    selected_rows = set(random.sample(range(rows), rows // 2))

    for r in range(rows):
        source = parent1 if r in selected_rows else parent2

        for c in range(cols):
            if fixed_mask[r][c]:
                child[r][c] = parent1[r][c]     # keep the original clue from the board
            else:
                child[r][c] = source[r][c]

    return child

# column based crossover
def col_based_crossover(parent1, parent2, fixed_mask):
    rows = len(parent1)
    cols = len(parent1[0])

    child = [[-1 for _ in range(cols)] for _ in range(rows)]
    selected_cols = set(random.sample(range(cols), cols // 2))

    for c in range(cols):
        source = parent1 if c in selected_cols else parent2

        for r in range(rows):
            if fixed_mask[r][c]:
                child[r][c] = parent1[r][c]     # keep the original clue from the board
            else:
                child[r][c] = source[r][c]

    return child


'''
    Mutation using neighbourhood-based
'''
def mutate(board, fixed_mask):
    conflicts = get_conflict_cells(board)

    if not conflicts:
        return

    # filter yang bisa diubah
    candidates = [(r, c) for (r, c) in conflicts if not fixed_mask[r][c]]

    if not candidates:
        return

    values = [board[r][c] for (r, c) in candidates]

    # ===== CASE 1: ada 2 warna → swap =====
    if len(candidates) >= 2 and (0 in values and 1 in values):
        (r1, c1), (r2, c2) = random.sample(candidates, 2)

        if board[r1][c1] != board[r2][c2]:
            board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
            return

    # ===== CASE 2: fallback → flip =====
    r, c = random.choice(candidates)
    board[r][c] = 1 - board[r][c]


# get all conflicted cells
def get_conflict_cells(board):
    rows = len(board)
    cols = len(board[0])
    conflicts = []

    # check triplet
    for r in range(rows):
        for c in range(cols - 2):
            if board[r][c] == board[r][c+1] == board[r][c+2]:
                conflicts.extend([(r,c), (r,c+1), (r,c+2)])

    for c in range(cols):
        for r in range(rows - 2):
            if board[r][c] == board[r+1][c] == board[r+2][c]:
                conflicts.extend([(r,c), (r+1,c), (r+2,c)])

    return list(set(conflicts))


'''
    Main Genetic Algorithm loop
'''
def run_genetic(base_board, fixed_mask, difficulty):
    population = init_population(base_board, fixed_mask, POPULATION_SIZE)

    best = None
    best_score = float('-inf')

    for gen in range(MAX_GENERATIONS):
        new_population = []

        # elitism
        population.sort(key=lambda x: fitness(x), reverse=True)
        best_current = population[0]
        best_current_score = fitness(best_current)

        if best_current_score > best_score:
            best = copy.deepcopy(best_current)
            best_score = best_current_score
            print(f"[best fitness current] {best_score}")

        if best_score == 0:
            return best
        
        new_population.append(copy.deepcopy(best_current))     # elisitm

        pairs = selection(population, POPULATION_SIZE-1)

        for parent1, parent2 in pairs:
            if random.random() < CROSSOVER_RATE:
                child = crossover(parent1, parent2, fixed_mask)
            else:
                child = copy.deepcopy(
                    parent1 if fitness(parent1) > fitness(parent2) else parent2
                )

            if random.random() < MUTATION_RATE:
                mutate(child, fixed_mask)

            new_population.append(child)

            if len(new_population) >= POPULATION_SIZE:
                break

        population = new_population

    print(f"[end of Genetic Algorithm]\n")
    return best