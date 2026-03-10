# Checkers AI (Italian Draughts)

**Author:** Federica Di Dio  
**Course:** Artificial Intelligence - University of Catania - Master's Degree in Computer Science

A Python implementation of Italian Draughts, allowing a human player to compete against an intelligent agent powered by the Minimax algorithm with Alpha-Beta pruning.

## Features
* **AI Engine**: Utilizes the Minimax algorithm to determine the optimal move by anticipating the opponent's counter-moves.
* **Optimization**: Implements Alpha-Beta pruning to explore the game tree efficiently, discarding non-promising branches to minimize computation time.
* **Advanced Heuristics**: The evaluation function calculates the score by weighing material and positional advantages (e.g., progression towards king promotion).
* **Robustness**: Includes input error handling via try-except blocks and rigorous move validation to ensure compliance with official rules.

## Project Logic
The game is modeled on an 8x8 board with a weighted scoring hierarchy:
* **Pawn**: 10 base points + advancement bonus.
* **King**: 20 base points + doubled positional bonus.
* **Terminal States**: Infinite values assigned for win/loss conditions to terminate recursion.



The default search depth is set to 4, balancing decision quality with immediate response times.

## Getting Started
1. Ensure you have Python installed.
2. Download the `dama.py` file.
3. Run the game from your terminal: `python dama.py`

## Gameplay Instructions
When it is your turn, enter your move coordinates in the following format:
`start_row start_column end_row end_column`

*(Example: `5 1 4 2` to move from cell (5,1) to (4,2))*

## Documentation
For an in-depth analysis of the problem modeling, software architecture, and the mathematical details of the algorithm, please refer to the *[Project Report](Relazione.pdf)* included in the repository. 

*Note: The documentation is currently available in Italian.*
