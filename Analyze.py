import os
import re
from statistics import mean, stdev

# MODE = "5.3.1"        # preprocessing
# MODE = "5.3.2.1"      # preprocessing + heuristic 1
# MODE = "5.3.2.2"      # preprocessing + heuristic 2
# MODE = "5.3.2.3"      # preprocessing + heuristic 3
# MODE = "5.3.3.1"      # preprocessing + GA param kecil
# MODE = "5.3.3.2"      # preprocessing + GA param besar
# MODE = "5.3.3.3"      # preprocessing + GA param tuning
# MODE = "5.3.4.1"      # preprocessing + GA weight tetap
# MODE = "5.3.4.2"      # preprocessing + GA weight tuning
MODE = "5.3.5"        # preprocessing + heuristic + GA

ROOT_DIR = "Answer"
EXPERIMENT = MODE

fitness_pattern = re.compile(r"Fitness\s*:\s*([-+]?\d*\.?\d+)")
time_pattern = re.compile(r"Time\s*:\s*([-+]?\d*\.?\d+)")

experiment_path = os.path.join(ROOT_DIR, EXPERIMENT)

for folder_name in sorted(os.listdir(experiment_path)):
    folder_path = os.path.join(experiment_path, folder_name)

    if not os.path.isdir(folder_path):
        continue

    fitness_list = []
    time_list = []

    total_boards = 0
    success_boards = 0
    fail_boards = 0

    for file_name in os.listdir(folder_path):
        if not file_name.endswith(".txt"):
            continue

        total_boards += 1
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        fitness_match = fitness_pattern.search(content)
        time_match = time_pattern.search(content)

        if fitness_match:
            fitness_value = float(fitness_match.group(1))
            fitness_list.append(fitness_value)

            if fitness_value == 0:
                success_boards += 1
            else:
                fail_boards += 1

        if time_match:
            time_list.append(float(time_match.group(1)))

    success_rate = (success_boards / total_boards * 100 if total_boards > 0 else 0)

    print(f"\n=== {folder_name} ===")
    print(f"Total Board : {total_boards}")
    print(f"Success     : {success_boards}")
    print(f"Fail        : {fail_boards}")
    print(f"Success Rate: {success_rate:.2f}%")

    if fitness_list:
        print(f"Max Fitness : {max(fitness_list):.4f}")
        print(f"Min Fitness : {min(fitness_list):.4f}")
        print(f"Avg Fitness : {mean(fitness_list):.4f}")

    if time_list:
        print(f"Avg Time    : {mean(time_list):.4f} sec")

    if len(fitness_list) > 1:
        print(f"Std Fitness : {stdev(fitness_list):.4f}")