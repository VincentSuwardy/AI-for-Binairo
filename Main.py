import random
from WebIterator import WebInteractor, URL

class DummyAnswer:
    class State:
        def __init__(self, board):
            self.board = board
    def __init__(self, board):
        self.state = self.State(board)

def main():
    # inisialisasi objek iterator
    iterator = WebInteractor(URL)

    # ambil puzzle
    size = "6"  # ukuran: 6, 8, 10, 14, 20
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
        print(" ".join(row))

    # simpan puzzle ke file local
    iterator.save_puzzle(id, board, size, difficulty)

    random_board = [[random.choice([0, 1]) for _ in range(int(size))] for _ in range(int(size))]
    
    random_answer = DummyAnswer(random_board)

    iterator.input_answer(random_answer)

    # iterator.close()

if __name__ == "__main__":
    main()