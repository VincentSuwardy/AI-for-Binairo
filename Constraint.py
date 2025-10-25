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
        # changed |= pattern_4(board)
        # changed |= pattern_5(board)
        # changed |= pattern_6(board)
        # changed |= pattern_7(board)

    return board

# random fills
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

# game patterns
'''
    Pattern 0:
    Setiap baris/kolom harus bersifat unik.
    Tidak diperbolehkan ada dua baris/kolom identik.
'''
def pattern_0(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
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

'''
def pattern_4(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed

'''

'''
def pattern_5(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed

'''

'''
def pattern_6(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed

'''

'''
def pattern_7(board):
    size = len(board)
    changed = False

    # TODO: implement algorithm
    
    return changed
