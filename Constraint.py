EMPTY = -1
WHITE = 0
BLACK = 1

'''
    Terapkan constraint patterns ke board.
    @params Board = 2D list of strings, "-1" = kosong, "0" = putih, "1" = hitam
    @return: board yang sudah di-update dengan aturan yang bisa diterapkan
'''
def apply_constraints(board):
    size = len(board)
    changed = True

    while changed:
        changed = False

        # apply rules
        # changed |= pattern_0(board)
        changed |= pattern_1(board)
        changed |= pattern_2(board)
        changed |= pattern_3(board)

    return board

# game patterns

'''
    Pattern 0:
    Setiap baris/kolom harus bersifat unik.
    Tidak diperbolehkan ada dua baris/kolom identik.
'''
def pattern_0(board):
    size = len(board)
    changed = False

    # helper: fill empty cell(s) so there's no duplicate
    def fill_row_constraint(row, full_rows, row_idx=None, col_idx=None):
        empty_idx = [i for i, v in enumerate(row) if v == EMPTY]
        if not empty_idx:
            return False
        
        # generate all combinations, fill -1 with 0/1
        from itertools import product
        possible_fills = list(product([WHITE, BLACK], repeat=len(empty_idx)))
        for fill in possible_fills:
            temp_row = row.copy()
            for idx, val in zip(empty_idx, fill):
                temp_row[idx] = val
            if temp_row not in full_rows:
                candidate = temp_row
                break
        else:
            return False    # no valid combination found
        
        # check if candidate different with original
        if candidate != row:
            for i, idx in enumerate(empty_idx):
                old_val = row[idx]
                row[idx] = candidate[idx]
                loc = f"Row {row_idx}" if row_idx is not None else f"Col {col_idx}"
                print(f"[pattern_0] {loc} col {idx} changed {old_val} -> {row[idx]}")
            return True
        return False
    
    # take all full rows
    full_rows = [row for row in board if EMPTY not in row]

    # process rows
    for r in range(size):
        if EMPTY in board[r]:
            if fill_row_constraint(board[r], full_rows, row_idx=r):
                changed = True

    # process columns
    transposed = [[board[r][c] for r in range(size)] for c in range(size)]
    full_cols = [col for col in transposed if EMPTY not in col]

    for c in range(size):
        if EMPTY in transposed[c]:
            if fill_row_constraint(transposed[c], full_cols, col_idx=c):
                # rewrite board
                for r in range(size):
                    old_val = board[r][c]
                    board[r][c] = transposed[c][r]
                    if old_val != board[r][c]:
                        print(f"[pattern_0] Col {c} row {r} changed {old_val} -> {board[r][c]}")
                changed = True
    
    return changed


'''
    Pattern 1:
    Tidak boleh ada 3 bidak dengan warna yang sama.
    Tutup semua ujung bidak yang adjecency dengan bidak warna berbeda.

    _ 0 0 _ to 1 0 0 1 
'''
def pattern_1(board):
    size = len(board)
    changed = False

    # check row
    for r in range(size):
        for c in range(size-2):
            triple = board[r][c:c+3]

            # if there are 2 same colors, and one empty in the edge
            if triple[0] == triple[1] != EMPTY and triple[2] == EMPTY:
                old = board[r][c+2]
                board[r][c+2] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_1] Row {r} col {c+2} changed {old} -> {board[r][c+2]}")
                changed = True
            if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                old = board[r][c]
                board[r][c] = WHITE if triple[1] == BLACK else BLACK
                print(f"[pattern_1] Row {r} col {c} changed {old} -> {board[r][c]}")
                changed = True

    # check column
    for c in range(size):
        for r in range(size - 2):
            triple = [board[r+i][c] for i in range(3)]

            if triple[0] == triple[1] != EMPTY and triple[2] == EMPTY:
                old = board[r+2][c]
                board[r+2][c] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_1] Col {c} row {r+2} changed {old} -> {board[r+2][c]}")
                changed = True
            if triple[1] == triple[2] != EMPTY and triple[0] == EMPTY:
                old = board[r][c]
                board[r][c] = WHITE if triple[1] == BLACK else BLACK
                print(f"[pattern_1] Col {c} row {r} changed {old} -> {board[r][c]}")
                changed = True

    return changed


'''
    Pattern 2:
    Tidak boleh ada 3 bidak dengan warna yang sama.
    Halangi bidak dengan jeda 1 kotak, dengan bidak warna lain.

    0 _ 0 to 0 1 0
'''
def pattern_2(board):
    size = len(board)
    changed = False

    # check row
    for r in range(size):
        for c in range(size - 2):
            triple = board[r][c:c+3]
            if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                old = board[r][c+1]
                board[r][c+1] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_2] Row {r} col {c+1} changed {old} -> {board[r][c+1]}")
                changed = True

    # check column
    for c in range(size):
        for r in range(size - 2):
            triple = [board[r+i][c] for i in range(3)]
            if triple[0] == triple[2] != EMPTY and triple[1] == EMPTY:
                old = board[r+1][c]
                board[r+1][c] = WHITE if triple[0] == BLACK else BLACK
                print(f"[pattern_2] Col {c} row {r+1} changed {old} -> {board[r+1][c]}")
                changed = True

    return changed


'''
    Pattern 3:
    Setiap baris/kolom harus memiliki jumlah hitam dan putih yang sama.
    Isi otomatis jika salah satu warna sudah setengah penuh.
'''
def pattern_3(board):
    size = len(board)
    changed = False
    half = size // 2

    # check row
    for r in range(size):
        row = board[r]
        if row.count(WHITE) == half:
            for c in range(size):
                if row[c] == EMPTY:
                    old = row[c]
                    row[c] = BLACK
                    print(f"[pattern_3] Row {r} col {c} changed {old} -> BLACK")
                    changed = True
        elif row.count(BLACK) == half:
            for c in range(size):
                if row[c] == EMPTY:
                    old = row[c]
                    row[c] = WHITE
                    print(f"[pattern_3] Row {r} col {c} changed {old} -> WHITE")
                    changed = True
    
    # check column
    for c in range(size):
        col = [board[r][c] for r in range(size)]
        if col.count(WHITE) == half:
            for r in range(size):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = BLACK
                    print(f"[pattern_3] Col {c} row {r} changed {old} -> BLACK")
                    changed = True
        elif col.count(BLACK) == half:
            for r in range(size):
                if board[r][c] == EMPTY:
                    old = board[r][c]
                    board[r][c] = WHITE
                    print(f"[pattern_3] Col {c} row {r} changed {old} -> WHITE")
                    changed = True

    return changed


'''
    Fill empty cells with random 0 or 1
'''
def fill_random(board):
    import random
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c] == EMPTY:
                old = board[r][c]
                board[r][c] = random.choice([WHITE, BLACK])
                print(f"[fill_random] Row {r} col {c} changed {old} -> {board[r][c]}")
    return board
