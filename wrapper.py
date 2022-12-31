import os
from ctypes import CDLL, c_int8, c_uint8, c_uint16
from numpy.ctypeslib import ndpointer
import numpy as np

class CWrapper():
    def __init__(self):
        os.system('gcc -fpic -shared -o solver.so solver.c')

        self.lib = CDLL("./solver.so")
        self._getBestMove_fun = self.lib.getBestMove

        c_int8_ptr = ndpointer(c_int8, flags="C_CONTIGUOUS")
        c_uint8_ptr = ndpointer(c_uint8, flags="C_CONTIGUOUS")

        self._getBestMove_fun.restype = None
        self._getBestMove_fun.argtypes = [c_int8_ptr, c_uint16, c_uint16, c_uint8_ptr, c_uint8]

    def getBestMove(self, grid):
        moves_limit = 5
        grid_np = np.array(grid, dtype=np.int8)
        best_moves = np.zeros(moves_limit * 3, dtype=np.uint8)

        self._getBestMove_fun(grid_np, *grid_np.shape, best_moves, moves_limit)
        best_moves = np.split(best_moves, best_moves.size / 3)

        moves_to_do = []
        for move in best_moves:
            if np.sum(move) != 0:
                moves_to_do.append(
                    [bool(move[0]), [move[1], move[2]]]
                )

        return moves_to_do
