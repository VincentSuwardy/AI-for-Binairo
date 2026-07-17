# AI for Binairo

An AI-based Binairo (Takuzu) puzzle solver that combines **Constraint Satisfaction**, **Heuristic Search**, and a **Genetic Algorithm** to solve logic puzzles of various sizes and difficulty levels.

> This project was developed as the final undergraduate thesis for the Artificial Intelligence course.

**Author**  
Vincent Emmanuel Suwardy (6182201067)

**Supervisor**  
Lionov, S.Kom., M.Sc., Ph.D.

---

## Overview

Binairo (also known as **Takuzu**) is a binary logic puzzle where each cell must be filled with either black or white while satisfying several logical constraints.

This project proposes a hybrid solving approach by combining deterministic preprocessing with heuristic-guided search and a Genetic Algorithm to improve solving performance on difficult puzzles.

Puzzle source:

https://www.puzzle-binairo.com/

---

## Binairo Rules

A valid Binairo board must satisfy the following rules:

1. Every row and column contains an equal number of black and white cells.
2. No more than two identical colors may appear consecutively.
3. Every row and every column must be unique.

---

## Features

- Automatic puzzle scraping using Selenium
- Support for puzzle sizes:
  - 6×6
  - 8×8
  - 10×10
  - 14×14
  - 20×20
  - Daily (24×24)
  - Weekly (30×30)
  - Monthly (30×40)
- Constraint-based preprocessing
- Multiple heuristic strategies
- Genetic Algorithm solver
- Adaptive GA parameters
- Adaptive fitness weight tuning
- Automatic solution validation
- Performance analysis tools

---

## Solver Pipeline

```
Retrieve Puzzle
       │
       ▼
Constraint Preprocessing
       │
       ▼
Heuristic Search
       │
       ▼
Genetic Algorithm
       │
       ▼
Validation
       │
       ▼
Save Solution
```

---

## Project Structure

```
.
├── Main.py               # Main application
├── WebInteractor.py      # Puzzle scraping & submission
├── Constraint.py         # Constraint propagation rules
├── Heuristic.py          # Heuristic preprocessing
├── Genetic.py            # Genetic Algorithm solver
├── Validator.py          # Solution validator
├── Tester.py             # Batch experiment runner
├── Analyze.py            # Experimental result analyzer
├── Data/                 # Downloaded puzzle datasets
└── Answer/               # Solver outputs
```

---

## Solving Approach

### 1. Constraint Satisfaction

The solver first applies deterministic constraint propagation to reduce the search space.

Implemented rules include:

- Color balancing
- Three-adjacent rule
- Uniqueness rule
- Additional advanced logical patterns

---

### 2. Heuristic Search

When deterministic rules are no longer sufficient, heuristic methods are used to generate promising board states.

Implemented heuristics include:

- Most Constrained Cell
- Density-based Fill
- Line Possibility Analysis

---

### 3. Genetic Algorithm

The remaining search space is solved using a Genetic Algorithm featuring:

- Population initialization
- Firefly-inspired parent selection
- Row-based crossover
- Column-based crossover
- Neighborhood mutation
- Elite preservation
- Adaptive parameter tuning
- Adaptive fitness weighting

---

## Running the Project

Install Selenium

```bash
pip install selenium
```

Configure the puzzle size and difficulty inside `Main.py`.

Example:

```python
PUZZLE_SIZE = "20"
PUZZLE_DIFF = "hard"
```

Run:

```bash
python Main.py
```

---

## Output

Downloaded puzzles are stored in

```
Data/
```

Generated solutions are stored in

```
Answer/
```

Each generated solution contains:

- Puzzle ID
- Puzzle size
- Difficulty
- Genetic Algorithm parameters
- Fitness weights
- Final board
- Fitness value
- Execution time

---

## Experiment Utilities

### Tester.py

Runs benchmark experiments for multiple solver configurations.

### Analyze.py

Calculates:

- Success rate
- Average fitness
- Standard deviation
- Average execution time

---

## Technologies

- Python
- Selenium
- Genetic Algorithm
- Constraint Satisfaction
- Heuristic Search

---

## License

This project was developed for academic and research purposes.
