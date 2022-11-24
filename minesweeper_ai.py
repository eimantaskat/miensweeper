from minesweeper import Minesweeper
import numpy as np
import copy
import keyboard
import time

class msai():
    def __init__(self):
        # self.grid = [[ 0,  1, -1, -1, -1, -1, -1, -1],
        #              [ 0,  1, -1, -1, -1, -1, -1, -1],
        #              [ 1,  3, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1],
        #              [-1, -1, -1, -1, -1, -1, -1, -1]]

        self.possibleVariants = []

    def _tiles_around(self, x, y):
        if x == 0:
            # first column
            if y == 0:
                # first line
                return [[x, y+1], [x+1, y], [x+1, y+1]]

            elif y == len(self.grid) - 1:
                # last line
                return [[x, y-1], [x+1, y-1], [x+1, y]]

            else:
                # mid lines
                return [[x, y-1], [x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1]]

        elif x == len(self.grid[0]) - 1:
            # last column
            if y == 0:
                # first line
                return [[x, y+1], [x-1, y], [x-1, y+1]]

            elif y == len(self.grid) - 1:
                # last line
                return [[x-1, y], [x-1, y-1], [x, y-1]]

            else:
                # mid lines
                return [[x, y-1], [x-1, y-1], [x-1, y], [x-1, y+1], [x, y+1]]

        else:
            # mid columns
            if y == 0:
                # first line
                return [[x-1, y], [x-1, y+1], [x, y+1], [x+1, y+1], [x+1, y]]

            elif y == len(self.grid) - 1:
                # last line
                return [[x-1, y], [x-1, y-1], [x, y-1], [x+1, y-1], [x+1, y]]

            else:
                # mid lines
                return [[x-1, y], [x-1, y-1], [x, y-1], [x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1], [x-1, y+1]]


    def _find_mines(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        unknown, mines = 0, 0
        mine = []
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] == -1:
                unknown += 1
                mine.append([y, x])
            elif self.grid[x][y] == 9 or self.grid[x][y] == 19:
                mines += 1

        
        if unknown == self.grid[y0][x0] - mines:
            return mine
        else:
            return None

    def _find_safe(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        unknown, mines = 0, 0
        safe = []
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] == -1:
                unknown += 1
                safe.append([y, x])
            elif self.grid[x][y] == 9 or self.grid[x][y] == 19:
                mines += 1

        
        if self.grid[y0][x0] - mines == 0:
            return safe
        else:
            return None

    def _remove_duplicates(self, list):
        newList = []
        for i in list:
            if i not in newList:
                newList.append(i)
        return newList

    def solve(self, grid, mine_count, ms):
        self.grid = grid
        mines = []
        safe = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] != -1 and self.grid[y][x] != 0:
                    if m := self._find_mines(x, y):
                        mines += m

                    elif s := self._find_safe(x, y):
                        safe += s

        mines = self._remove_duplicates(mines)
        safe = self._remove_duplicates(safe)

        for tile in mines:
            ms.click(tile[0], tile[1], False)

        for tile in safe:
            ms.click(tile[0], tile[1], True)

        if len(mines) + len(safe) == 0:
            n = len(self.grid)
            m = len(self.grid[0])

            if self.grid[0][0] == -1:
                ms.click(0, 0, True)
            # elif self.grid[0][m - 1] == -1:
            #     ms.click(m - 1, 0, True)
            # elif self.grid[n - 1][0] == -1:
            #     ms.click(0, n - 1, True)
            # elif self.grid[n - 1][m - 1] == -1:
            #     ms.click(m - 1, n - 1, True)

            else:
                # tic = time.perf_counter()
                is_safe, tile = self.calculatePossibilities()
                # toc = time.perf_counter()
                # print(f"Calculated probabilities in {toc - tic:0.4f} seconds")
                print(tile)
                time.sleep(1)
                ms.click(tile[0], tile[1], is_safe)

        # print("mines", mines, "\nsafe", safe)
        return self.grid

    def _has_adj_num(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        tiles_with_num = 0
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] > 0 and self.grid[x][y] < 9:
                tiles_with_num += 1

        
        if tiles_with_num == 0:
            return False
        else:
            return True

    def _missing_mine(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        mines = 0
        for tile in adj_tiles:
            y, x = tile

            if self.grid[x][y] == 9 or self.grid[x][y] == 19:
                mines += 1
        
        return self.grid[y0][x0] > mines

    def _can_be_mine(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)

        for tile in adj_tiles:
            x, y = tile
            if not self._missing_mine(x, y) and self.grid[y][x] != -1:
                return False

        return True


    def _adj_mines(self, x0, y0):
        adj_tiles = self._tiles_around(x0, y0)
        
        mines = 0
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] == 9 or self.grid[x][y] == 19:
                mines += 1

        return mines

    def _adj_unknown(self, x0, y0):
        adj_tiles = self._tiles_around( x0, y0)
        
        unknown = 0
        
        for tile in adj_tiles:
            y, x = tile
            if self.grid[x][y] == -1:
                unknown += 1

        return unknown

    def _is_valid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] > 0 and self.grid[y][x] < 9:
                    mines = self._adj_mines(x, y)
                    if self.grid[y][x] < mines or self.grid[y][x] - mines > self._adj_unknown(x, y):
                        return False
        return True

    def set_grid(self, grid):
        self.grid = grid

    def _possibilities(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == -1 and self._has_adj_num(x, y):
                    for n in (19, 10):
                        self.grid[y][x] = n

                        if self._is_valid():
                            self._possibilities()
                        
                        self.grid[y][x] = -1
                    return

        self.appendList(copy.deepcopy(self.grid))

    def appendList(self, list):
        self.possibleVariants.append(list)

    def calculatePossibilities(self):
        self.possibleVariants = []
        self._possibilities()

        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                for grid in self.possibleVariants:
                    if grid[y][x] == 19:
                        grid[y][x] = 1
                    elif grid[y][x] == 10:
                        grid[y][x] = -1
                    else:
                        grid[y][x] = 0
                    
        probabilityMatrix = np.array([ [0] * len(self.grid[0]) ] * len(self.grid))

        for grid in self.possibleVariants:
            probabilityMatrix = np.add(probabilityMatrix, np.array(grid))

        probabilityMatrix = probabilityMatrix.tolist()

        # for i in range(len(probabilityMatrix)):
        #     for j in range(len(probabilityMatrix[0])):
        #         probabilityMatrix[i][j] /= len(self.possibleVariants)
            
        # -1 100% safe
        # 1  100% mine

        mine, mineX, mineY = probabilityMatrix[0][0], 0, 0
        safe, safeX, safeY = probabilityMatrix[0][0], 0, 0

        allSafe = []
        allMines = []

        for i in range(len(probabilityMatrix)):
            for j in range(len(probabilityMatrix[0])):
                if probabilityMatrix[i][j] > mine:
                    mine = probabilityMatrix[i][j]
                    mineX = j
                    mineY = i
                elif probabilityMatrix[i][j] < safe:
                    safe = probabilityMatrix[i][j]
                    safeX = j
                    safeY = i

        # print(mine, mineX, mineY)
        # print(safe, safeX, safeY)
        
        if -1 * mine >= safe:
            return True, [safeX, safeY]
        else:
            return False, [mineX, mineY]



    
if __name__ == "__main__":
    ai = msai()

    # grid = [[ 0,  1, -1, -1, -1, -1, -1, -1],
    #         [ 0,  1, -1, -1, -1, -1, -1, -1],
    #         [ 1,  3, -1, -1, -1, -1, -1, -1],
    #         [-1, -1, -1, -1, -1, -1, -1, -1],
    #         [-1, -1, -1, -1, -1, -1, -1, -1],
    #         [-1, -1, -1, -1, -1, -1, -1, -1],
    #         [-1, -1, -1, -1, -1, -1, -1, -1],
    #         [-1, -1, -1, -1, -1, -1, -1, -1]]

    # ai.set_grid(grid)
    # ai.calculatePossibilities()


    ms = Minesweeper()
    while keyboard.is_pressed('q') == False and not ms.game_over():
        ai.solve(ms.get_grid(), 10, ms) 

    ms.game_over()