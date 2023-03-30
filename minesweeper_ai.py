import copy
import time
from random import randint

import keyboard
import numpy as np

from minesweeper import Minesweeper
from wrapper import CWrapper


class MinesweeperAI():
	def __init__(self):
		self.possible_variants = []
		self.wrapper = CWrapper()

	def _tiles_around(self, x, y):
		neighbors = []
		for i in range(x-1, x+2):
			for j in range(y-1, y+2):
				if i == x and j == y:
					continue
				if 0 <= i < len(self.grid[0]) and 0 <= j < len(self.grid):
					neighbors.append([i, j])
		return neighbors

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
		for tile in mines:
			ms.click(tile[0], tile[1], False)

		safe = self._remove_duplicates(safe)
		for tile in safe:
			ms.click(tile[0], tile[1], True)

		if len(mines) + len(safe) == 0:
			n = len(self.grid)
			m = len(self.grid[0])

			if self.grid[0][0] == -1:
				ms.click(0, 0, True)
			else:
				moves = self.wrapper.getBestMove(self.grid)

				for is_safe, tile in moves:
					time.sleep(.05)
					if np.sum(tile) != 0:
						ms.click(tile[0], tile[1], is_safe)
					else:
						if self.grid[0][m - 1] == -1:
							ms.click(m - 1, 0, True)
						elif self.grid[n - 1][0] == -1:
							ms.click(0, n - 1, True)
						elif self.grid[n - 1][m - 1] == -1:
							ms.click(m - 1, n - 1, True)
						else:
							x, y = randint(0, m-1), randint(0, n-1)
							while grid[y][x] != -1:
								x, y = randint(0, m-1), randint(0, n-1)
							ms.click(x, y, True)
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

	def _adj_mines(self, x0, y0):
		adj_tiles = self._tiles_around(x0, y0)

		mines = 0
		for tile in adj_tiles:
			y, x = tile
			if self.grid[x][y] == 9 or self.grid[x][y] == 19:
				mines += 1

		return mines

	def _adj_unknown(self, x0, y0):
		adj_tiles = self._tiles_around(x0, y0)

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

		self.append_list(copy.deepcopy(self.grid))

	def append_list(self, list):
		self.possible_variants.append(list)


if __name__ == "__main__":
	ai = MinesweeperAI()
	ms = Minesweeper()

	games = 100
	games_played = 0
	wins = 0
	losses = 0
	start = time.perf_counter()
	while not keyboard.is_pressed('q') and games_played < games:
		ms.start_game()

		while not keyboard.is_pressed('q') and not ms.game_over():
			ai.solve(ms.get_grid(), 10, ms)

		if ms.game_won():
			wins += 1
		elif ms.game_lost():
			losses += 1

		games_played += 1
		print(f"{games_played}/{games}")
	stop = time.perf_counter()

	print(f"Done in {stop - start}s")
	print(f"Average time to solve: {(stop - start)/games_played}s")
	print(f"Wins: {wins}")
	print(f"Losses: {losses}")
	print(f"Win%: {wins / games_played * 100}")
