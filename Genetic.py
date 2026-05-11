import random
import copy

EMPTY = -1
WHITE = 0
BLACK = 1

'''
    Genetic Algorithm hyperparameters in default value
'''
POPULATION_SIZE = 350
MAX_GENERATIONS = 800

MUTATION_RATE = 0.3
CROSSOVER_RATE = 0.95
ELITE_SIZE = 2

'''
    Adaptive Genetic Algorithm parameter
'''
def get_ga_params(rows, cols, difficulty=""):
    size = rows * cols

    # base scaling
    pop_size = int(1.5 * size)
    max_gen = int(3 * size)

    # adjust by difficulty
    if difficulty == "easy":
        pop_size = int(pop_size * 0.7)
        max_gen = int(max_gen * 0.7)
    elif difficulty == "hard":
        pop_size = int(pop_size * 1.5)
        max_gen = int(max_gen * 1.5)

    # limit to prevent overkill
    pop_size = min(max(pop_size, 50), 1000)
    max_gen = min(max(max_gen, 100), 2000)

    return pop_size, max_gen

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
                if not fixed_mask[r][c] and board[r][c] == EMPTY:
                    board[r][c] = random.choice([WHITE, BLACK])

        population.append(board)

    return population

'''
    count fitness function
    - for every triplets made,                penalty_1 += 1
    - count for balancing                     penalty_2 += |total_WHITE - total_BLACK|
    - for every duplicates row(s)/col(s),     penalty_3 += 1

    fitness = -(w1 * penalty_1) + (w2 * penalty_2) + (w3 * penalty_3)

    where wN is weight for every penalty
'''
def fitness(board, w1=20, w2=10, w3=1):
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

# Cache fitness to make program run faster
def cached_fitness(board, w1, w2, w3, cache):
    key = tuple(tuple(row) for row in board)

    if key not in cache:
        cache[key] = fitness(board, w1, w2, w3)
        # cache[key] = fitness(board)

    return cache[key]

'''
    "Auto-Tuning" Fitness Weights using Local Search
'''
def tune_fitness_weights(sample_board, fixed_mask, iterations=30):
    # initial weights
    current = [20, 10, 1]

    '''
        - initialize population
        - count every fitness
        - return average fitness in population
    '''
    def evaluate(weights):
        w1, w2, w3 = weights
        pop = init_population(sample_board, fixed_mask, 30)

        scores = [fitness(b, w1, w2, w3) for b in pop]
        return sum(scores) / len(scores)

    best_score = evaluate(current)

    # loop tuning
    for _ in range(iterations):
        candidate = current[:]

        # random tweak
        idx = random.randint(0, 2)
        '''
            - small step  (-1, +1): for soft fine-tuning
            - medium step (-2, +2): for larger exploration
            - big step    (-5, +5): further jump for escaping local optimum

            these combinations make:
            - exploration : search new area
            - exploitation: fixing current solution
        '''
        change = random.choice([-5, -2, -1, 1, 2, 5])
        candidate[idx] = max(1, candidate[idx] + change)

        score = evaluate(candidate)

        # accept better candidates
        # similar with hill climbing concept
        if score > best_score:
            current = candidate
            best_score = score
            print(f"[tuned weights] {current} score={best_score}")

    return current


'''
    Selection using Firefly Mating Algorithm
'''
def selection(population, num_pairs):
    pairs = []

    # count every indiv fitness
    fitness_values = [fitness(idx) for idx in population]
    # total_fit = sum(fitness_values)

    for _ in range(num_pairs):
        # random first parent
        i = random.randint(0, len(population)-1)
        parent1 = population[i]

        probs = []
        for j in range(len(population)):
            # if fitness_values[j] > fitness_values[i]:
            #     probs.append(fitness_values[j] - fitness_values[i])
            # else:
            #     probs.append(0)

            # attraction by fitness (firefly concept)
            diff = fitness_values[j] - fitness_values[i]
            probs.append(max(diff, 0))

        # select second parent
        if sum(probs) > 0:
            parent2 = random.choices(population, weights=probs, k=1)[0]
        else:
            parent2 = random.choice(population)

        # safe pairs
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
    # return uniform_crossover(parent1, parent2, fixed_mask)

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

# uniform crossover
def uniform_crossover(parent1, parent2, fixed_mask):
    rows = len(parent1)
    cols = len(parent1[0])

    child = [[-1]*cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if fixed_mask[r][c]:
                child[r][c] = parent1[r][c]
            else:
                if random.random() < 0.5:
                    child[r][c] = parent1[r][c]
                else:
                    child[r][c] = parent2[r][c]

    return child


'''
    Mutation using neighbourhood-based
'''
def mutate(board, fixed_mask):
    conflicts = get_conflict_cells(board)

    # Triplet-based mutation
    if conflicts:
        candidates = [(r, c) for (r, c) in conflicts if not fixed_mask[r][c]]

        if candidates:
            values = [board[r][c] for (r, c) in candidates]

            # swap kalau ada 2 warna
            if len(candidates) >= 2 and (0 in values and 1 in values):
                (r1, c1), (r2, c2) = random.sample(candidates, 2)

                if board[r1][c1] != board[r2][c2]:
                    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                    return

            # fallback flip dari conflict
            r, c = random.choice(candidates)
            board[r][c] = 1 - board[r][c]
            return

    # Balance-based mutation
    rows = len(board)
    cols = len(board[0])

    if random.random() < 0.5:
        # rows
        r = random.randint(0, rows - 1)

        whites = board[r].count(0)
        blacks = board[r].count(1)

        if whites != blacks:
            target = 0 if whites > blacks else 1

            candidates = [
                c for c in range(cols)
                if board[r][c] == target and not fixed_mask[r][c]
            ]

            if candidates:
                c = random.choice(candidates)
                board[r][c] = 1 - board[r][c]
                return

    else:
        # columns
        c = random.randint(0, cols - 1)

        col_vals = [board[r][c] for r in range(rows)]
        whites = col_vals.count(0)
        blacks = col_vals.count(1)

        if whites != blacks:
            target = 0 if whites > blacks else 1

            candidates = [
                r for r in range(rows)
                if board[r][c] == target and not fixed_mask[r][c]
            ]

            if candidates:
                r = random.choice(candidates)
                board[r][c] = 1 - board[r][c]
                return

    # Last fallback (random flip)
    r = random.randint(0, rows - 1)
    c = random.randint(0, cols - 1)

    if not fixed_mask[r][c]:
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
    rows = len(base_board)
    cols = len(base_board[0])

    POPULATION_SIZE, MAX_GENERATIONS = get_ga_params(rows, cols, difficulty)

    population = init_population(base_board, fixed_mask, POPULATION_SIZE)

    best = None
    best_score = float('-inf')
    fitness_cache = {}

    # tuning weights
    w1, w2, w3 = tune_fitness_weights(base_board, fixed_mask)

    for gen in range(MAX_GENERATIONS):
        new_population = []

        # elitism
        population.sort(
            key=lambda x: cached_fitness(x, w1, w2, w3, fitness_cache),
            reverse=True
        )

        best_current = population[0]
        best_current_score = cached_fitness(best_current, w1, w2, w3, fitness_cache)

        if best_current_score > best_score:
            best = copy.deepcopy(best_current)
            best_score = best_current_score
            print(f"[best fitness current] {best_score}")

        if best_score == 0:
            return best, best_score
        
        new_population.append(copy.deepcopy(best_current))     # elitism

        pairs = selection(population, POPULATION_SIZE-1)

        for parent1, parent2 in pairs:
            if random.uniform(0.0, 1.0) < CROSSOVER_RATE:
                child = crossover(parent1, parent2, fixed_mask)
            else:
                child = copy.deepcopy(
                    parent1 if fitness(parent1) > fitness(parent2) else parent2
                )

            if random.uniform(0.0, 1.0) <= MUTATION_RATE:
                mutate(child, fixed_mask)

            new_population.append(child)

            if len(new_population) >= POPULATION_SIZE:
                break

        population = new_population

    print(f"[stop] end of Genetic Algorithm\n")
    return best, best_score