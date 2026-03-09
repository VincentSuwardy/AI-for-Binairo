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

# Fungsol solve buat panggil heuristic
def solve_with_heuristic(board, difficulty):
    changed = True
    while changed:
        # apply deterministic constraints
        board = apply_constraints(board, difficulty)
        
        # kalau masih ada EMPTY, pakai heuristic fill
        # changed = fill_most_constrained_cell(board)
        changed = fill_based_on_local_balance(board)
    
    return board

# ======================================================================================================================
# Try heuristic random fill
# ======================================================================================================================
import random

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