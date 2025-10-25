import random
from WebIterator import WebInteractor, URL
from Constraint import apply_constraints, fill_random, EMPTY, WHITE, BLACK

class Answer:
    class State:
        def __init__(self, board):
            self.board = board
    def __init__(self, board):
        self.state = self.State(board)

def main():
    # inisialisasi objek iterator
    iterator = WebInteractor(URL)

    # ambil puzzle
    size = "14"  # ukuran: 6, 8, 10, 14, 20
    difficulty = "easy" # diff: easy, hard

    id, board = iterator.open_puzzle(size, difficulty)

    # cek hasil
    if not board:
        print("Fail to get puzzle")
        iterator.close()
        return
    
    print(f"Succesfully get puzzle")
    print("Board:")
    for row in board:
        print(" ".join(str(x) for x in row))

    # simpan puzzle ke file local
    iterator.save_puzzle(id, board, size, difficulty)

    # random_board = [[random.choice([0, 1]) for _ in range(int(size))] for _ in range(int(size))]
    # random_answer = DummyAnswer(random_board)

    board = apply_constraints(board)
    # board = fill_random(board)

    answer = Answer(board)
    iterator.save_answer(id, answer, size, difficulty)

    iterator.input_answer(answer)

    # iterator.close()

if __name__ == "__main__":
    main()