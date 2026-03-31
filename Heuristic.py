import random
from Constraint import apply_constraints

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

# Heuristic func
def apply_heuristic(board, difficulty):
    return solve_with_heuristic(board, difficulty)
    # return solve_with_limited_heuristic(board, difficulty)

# ======================================================================================================================
# Heuristic settings
# ======================================================================================================================

# Fungsi solve buat panggil heuristic
def solve_with_heuristic(board, difficulty):
    changed = True
    while changed:
        # apply deterministic constraints
        board = apply_constraints(board, difficulty)
        
        # kalau masih ada EMPTY, pakai heuristic fill
        # changed = fill_most_constrained_cell(board)
        changed = fill_based_on_local_balance(board)
        # changed = fill_with_hybrid_heuristic(board)
    
    return board

# Fungsi solver buat limit heuristic
def solve_with_limited_heuristic(board, difficulty, max_attempts=3):
    # Step 1: deterministic constraint awal
    board = apply_constraints(board, difficulty)

    # Step 2: loop heuristic + constraint beberapa kali
    counter = 0
    while counter < max_attempts:

        # changed = fill_most_constrained_cell(board)
        changed = fill_based_on_local_balance(board)
        # changed = fill_with_hybrid_heuristic(board)

        if not changed:
            break  # semua full / tidak ada cell tersisa

        board = apply_constraints(board, difficulty)
        counter += 1

    return board

# ======================================================================================================================
# Try heuristic most constrained cell fill
# ======================================================================================================================
'''
    1. Selalu pilih cell yang paling “terbatas” dulu, yaitu row atau column dengan jumlah EMPTY paling sedikit
    2. Dari kolom/kumpulan cell kosong itu, pilih cell yang paling terbatas lagi (EMPTY paling sedikit di kolom)
    3. Baru isi dengan random 0/1
'''

def fill_most_constrained_cell(board):
    size = len(board)
    # Step 1: cari row dengan EMPTY paling sedikit (tetapi > 0)
    min_empty_row = None
    min_empty_count = size + 1  # lebih besar dari max size
    for r in range(size):
        empty_count = board[r].count(EMPTY)
        if 0 < empty_count < min_empty_count:
            min_empty_count = empty_count
            min_empty_row = r

    if min_empty_row is None:
        # semua full, nothing to do
        return False

    # Step 2: dari EMPTY cell di row itu, cari yang kolomnya paling sedikit EMPTY
    candidates = [c for c in range(size) if board[min_empty_row][c] == EMPTY]
    best_c = candidates[0]
    min_empty_col = size + 1
    for c in candidates:
        col_empty_count = sum(1 for r in range(size) if board[r][c] == EMPTY)
        if col_empty_count < min_empty_col:
            min_empty_col = col_empty_count
            best_c = c

    # Step 3: isi dengan random 0/1
    old = board[min_empty_row][best_c]
    board[min_empty_row][best_c] = random.choice([WHITE, BLACK])
    debug_change("fill_most_constrained_cell", min_empty_row, best_c, old, board[min_empty_row][best_c])

    return True  # menandakan ada perubahan

# ======================================================================================================================
# Try heuristic balance fill
# ======================================================================================================================
'''
    1. Pilih cell yang paling constrained dari row/col (seperti sebelumnya).
    2. Dari cell itu, cek 3x3 area sekitar (neighboring 8 cells).
    3. Hitung kecenderungan warna: jumlah BLACK vs WHITE di area sekitar.
    4. Isi dengan warna yang lebih sedikit di area itu (supaya balance), kalau sama baru random.
'''
def fill_based_on_local_balance(board):
    size = len(board)
    # Step 1: cari row dengan EMPTY paling sedikit (tetapi > 0)
    min_empty_row = None
    min_empty_count = size + 1
    for r in range(size):
        empty_count = board[r].count(EMPTY)
        if 0 < empty_count < min_empty_count:
            min_empty_count = empty_count
            min_empty_row = r

    if min_empty_row is None:
        return False  # semua full

    # Step 2: dari EMPTY cell di row itu, cari yang kolomnya paling sedikit EMPTY
    candidates = [c for c in range(size) if board[min_empty_row][c] == EMPTY]
    best_c = candidates[0]
    min_empty_col = size + 1
    for c in candidates:
        col_empty_count = sum(1 for r in range(size) if board[r][c] == EMPTY)
        if col_empty_count < min_empty_col:
            min_empty_col = col_empty_count
            best_c = c

    r, c = min_empty_row, best_c

    # Step 3: cek area sekitar 3x3
    black_count = 0
    white_count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size and not (nr == r and nc == c):
                if board[nr][nc] == BLACK:
                    black_count += 1
                elif board[nr][nc] == WHITE:
                    white_count += 1

    # Step 4: pilih warna yang lebih sedikit, kalau sama random
    if black_count < white_count:
        color = BLACK
    elif white_count < black_count:
        color = WHITE
    else:
        color = random.choice([WHITE, BLACK])

    old = board[r][c]
    board[r][c] = color
    debug_change("fill_based_on_local_balance", r, c, old, color)

    return True

# ======================================================================================================================
# Try heuristic hybrid balance fill
# ======================================================================================================================
'''
1. Pilih cell paling “constrained” dulu (row & col paling sedikit EMPTY).
2. Cek sisa WHITE/BLACK di row dan col:
    - Misal row 5 sisa 2 WHITE, 3 BLACK
    - Col 3 sisa 1 WHITE, 3 BLACK
3. Tentukan warna berdasarkan yang lebih sedikit dari jumlah sisa terbesar antara row & col:
    - Row sisa terbesar = 3 (BLACK), col sisa terbesar = 3 (BLACK) → bandingkan masing-masing sisa: row 2 WHITE < 3 BLACK, col 1 WHITE < 3 BLACK → ambil yang lebih kecil (1 atau 2 WHITE) → pilih WHITE
    - Kalau jumlahnya sama, pakai heuristic lokal sebelumnya (cek neighbor 3x3).
'''
def fill_with_hybrid_heuristic(board):
    size = len(board)
    # Step 1: cari row dengan EMPTY paling sedikit (>0)
    min_empty_row = None
    min_empty_count = size + 1
    for r in range(size):
        empty_count = board[r].count(EMPTY)
        if 0 < empty_count < min_empty_count:
            min_empty_count = empty_count
            min_empty_row = r
    if min_empty_row is None:
        return False  # semua full

    # Step 2: dari EMPTY cell di row itu, cari col paling sedikit EMPTY
    candidates = [c for c in range(size) if board[min_empty_row][c] == EMPTY]
    best_c = candidates[0]
    min_empty_col = size + 1
    for c in candidates:
        col_empty_count = sum(1 for r in range(size) if board[r][c] == EMPTY)
        if col_empty_count < min_empty_col:
            min_empty_col = col_empty_count
            best_c = c

    r, c = min_empty_row, best_c

    # Step 3: cek sisa WHITE/BLACK di row dan col
    half = size // 2
    row_white_left = half - board[r].count(WHITE)
    row_black_left = half - board[r].count(BLACK)
    col_white_left = half - [board[rr][c] for rr in range(size)].count(WHITE)
    col_black_left = half - [board[rr][c] for rr in range(size)].count(BLACK)

    # Step 4: tentukan sisa maksimum di row & col
    max_row = max(row_white_left, row_black_left)
    max_col = max(col_white_left, col_black_left)

    # ambil warna yang lebih sedikit dari sisa maksimum
    row_color = WHITE if row_white_left < row_black_left else BLACK
    col_color = WHITE if col_white_left < col_black_left else BLACK

    chosen_color = None
    if max_row > max_col:
        chosen_color = row_color
    elif max_col > max_row:
        chosen_color = col_color
    else:
        # tie, fallback ke heuristic lokal neighbor 3x3
        black_count = 0
        white_count = 0
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < size and 0 <= nc < size and not (nr==r and nc==c):
                    if board[nr][nc] == BLACK:
                        black_count +=1
                    elif board[nr][nc] == WHITE:
                        white_count +=1
        if black_count < white_count:
            chosen_color = BLACK
        elif white_count < black_count:
            chosen_color = WHITE
        else:
            chosen_color = random.choice([WHITE, BLACK])

    old = board[r][c]
    board[r][c] = chosen_color
    debug_change("fill_with_hybrid_heuristic", r, c, old, chosen_color)

    return True