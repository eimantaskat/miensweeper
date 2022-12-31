from wrapper import CWrapper
from minesweeper_ai import msai

grid = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 2, 1, 1, 1, 1], [0, 1, 9, 9, 1, 2, 9, 3], [0, 1, 2, 2, 2, 3, 9, 9], [1, 1, 2, 1, 2, 9, 4, -1], [-1, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1]]
grid = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 2, 2, 1, 1, 1, 1], [0, 1, 9, 9, 1, 2, 9, 3], [0, 1, 2, 2, 2, 3, 9, 9], [1, 1, 2, 1, 2, 9, 4, -1], [10, -1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, -1, -1, -1, -1]]

# grid = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]

# ai = msai()
# ai.set_grid(grid)
# ai.calculate_possibilities()

wrapper = CWrapper()

wrapper.getBestMove(grid)
# print(wrapper.getBestMove(grid))

# wrapper.gridIsValid(grid)