#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

#define MAX_NEIGHBOUR_TILES 8
#define POSSIBLE_GUESSES_SIZE 2

struct tile
{
	uint16_t x;
	uint16_t y;
};

typedef struct tile tile;

uint16_t addTile(tile *tiles, const uint16_t posX, const uint16_t posY, uint16_t tilesSize)
{
	tile t = {posX, posY};
	tiles[tilesSize] = t;
	return ++tilesSize;
}

float largestNumber(float *arr, uint32_t size)
{
	double largest = abs(arr[0]);
	for (int i = 1; i < size; i++)
	{
		if (abs(arr[i]) > largest)
		{
			largest = abs(arr[i]);
		}
	}
	return largest;
}

uint16_t getNeighbourTiles(const uint16_t gridHeight, const uint16_t gridWidth, const uint16_t posX, const uint16_t posY, tile *tiles, uint16_t tilesSize)
{
	const int deltaX[] = {0, 1, 1, 1, 0, -1, -1, -1};
	const int deltaY[] = {1, 1, 0, -1, -1, -1, 0, 1};

	for (int i = 0; i < 8; ++i)
	{
		const int x = posX + deltaX[i];
		const int y = posY + deltaY[i];

		if (x >= 0 && x < gridWidth && y >= 0 && y < gridHeight)
		{
			tilesSize = addTile(tiles, x, y, tilesSize);
		}
	}

	return tilesSize;
}

uint8_t getAdjacentMinesNum(const int8_t *grid, const uint16_t gridHeight, const uint16_t gridWidth, const uint16_t posX, const uint16_t posY)
{
	uint16_t tilesSize;
	uint8_t mines;
	tile *tiles = (tile *)malloc(MAX_NEIGHBOUR_TILES * sizeof(tile));

	tilesSize = getNeighbourTiles(gridHeight, gridWidth, posX, posY, tiles, 0);
	mines = 0;

	for (uint16_t i = 0; i < tilesSize; i++)
	{
		uint16_t x = tiles[i].x;
		uint16_t y = tiles[i].y;

		if (grid[x + gridWidth * y] == 9 || grid[x + gridWidth * y] == 19)
		{
			mines++;
		}
	}

	free(tiles);
	return mines;
}

uint8_t getUnknownTilesNum(const int8_t *grid, const uint16_t gridHeight, const uint16_t gridWidth, const uint16_t posX, const uint16_t posY)
{
	uint16_t tilesSize;
	uint8_t unknown;
	tile *tiles = (tile *)malloc(MAX_NEIGHBOUR_TILES * sizeof(tile));

	tilesSize = getNeighbourTiles(gridHeight, gridWidth, posX, posY, tiles, 0);
	unknown = 0;

	for (uint16_t i = 0; i < tilesSize; i++)
	{
		uint16_t x = tiles[i].x;
		uint16_t y = tiles[i].y;

		if (grid[x + gridWidth * y] == -1)
		{
			unknown++;
		}
	}

	free(tiles);
	return unknown;
}

bool hasAdjacentNumber(const int8_t *grid, const uint16_t gridHeight, const uint16_t gridWidth, const uint16_t posX, const uint16_t posY)
{
	uint16_t tilesSize;
	uint8_t tilesWithNumber;
	tile *tiles = (tile *)malloc(MAX_NEIGHBOUR_TILES * sizeof(tile));

	tilesSize = getNeighbourTiles(gridHeight, gridWidth, posX, posY, tiles, 0);
	tilesWithNumber = 0;

	for (uint16_t i = 0; i < tilesSize; i++)
	{
		uint16_t x = tiles[i].x;
		uint16_t y = tiles[i].y;

		if ((grid[x + gridWidth * y] > 0) && (grid[x + gridWidth * y] < 9))
		{
			tilesWithNumber++;
		}
	}
	if (tilesWithNumber)
	{
		return true;
	}
	return false;
	free(tiles);
}

bool gridIsValid(const int8_t *grid, const uint16_t gridHeight, const uint16_t gridWidth)
{
	uint8_t minesNum;
	uint8_t unknownNum;
	for (uint16_t y = 0; y < gridHeight; y++)
	{
		for (uint16_t x = 0; x < gridWidth; x++)
		{
			if ((grid[x + gridWidth * y] > 0) && (grid[x + gridWidth * y] < 9))
			{
				minesNum = getAdjacentMinesNum(grid, gridHeight, gridWidth, x, y);
				unknownNum = getUnknownTilesNum(grid, gridHeight, gridWidth, x, y);

				if ((grid[x + gridWidth * y] < minesNum) || ((grid[x + gridWidth * y] - minesNum) > unknownNum))
				{
					return false;
				}
			}
		}
	}
	return true;
}

void getPossibilities(int8_t *grid, const uint16_t gridHeight, const uint16_t gridWidth, float *probabilityMatrix, int32_t *possibleSolutionsCount, tile *t)
{
	uint8_t guesses[POSSIBLE_GUESSES_SIZE] = {19, 10};

	for (uint16_t y = 0; y < gridHeight; y++)
	{
		for (uint16_t x = 0; x < gridWidth; x++)
		{
			bool hasAdjNum = hasAdjacentNumber(grid, gridHeight, gridWidth, x, y);

			if ((grid[x + gridWidth * y] == -1) && hasAdjNum)
			{
				for (uint8_t i = 0; i < POSSIBLE_GUESSES_SIZE; i++)
				{
					grid[x + gridWidth * y] = guesses[i];

					bool isValid = gridIsValid(grid, gridHeight, gridWidth);
					if (isValid)
					{
						getPossibilities(grid, gridHeight, gridWidth, probabilityMatrix, possibleSolutionsCount, t);
					}

					grid[x + gridWidth * y] = -1;
				}
				return;
			}
		}
	}

	for (uint16_t y = 0; y < gridHeight; y++)
	{
		for (uint16_t x = 0; x < gridWidth; x++)
		{
			uint32_t i = x + gridWidth * y;
			if (grid[i] == 19)
			{
				probabilityMatrix[i]--;
			}
			else if (grid[i] == 10)
			{
				probabilityMatrix[i]++;
				t->x = x;
				t->y = y;
			}
		}
	}
	(*possibleSolutionsCount)++;
}

void getBestMove(int8_t *grid, const uint16_t gridHeight, const uint16_t gridWidth, uint8_t *bestMoves, uint8_t movesLimit)
{
	float *probabilityMatrix;
	int32_t possibleSolutionsCount;
	uint16_t bestMovesSize;
	tile t;

	probabilityMatrix = (float *)calloc(gridHeight * gridWidth, sizeof(float));
	possibleSolutionsCount = 0;
	bestMovesSize = 0;

	getPossibilities(grid, gridHeight, gridWidth, probabilityMatrix, &possibleSolutionsCount, &t);

	for (uint32_t i = 0; i < gridHeight * gridWidth; i++)
	{
		probabilityMatrix[i] /= possibleSolutionsCount;
	}

	float highestProbability = largestNumber(probabilityMatrix, gridHeight * gridWidth);
	if (!highestProbability)
	{
		bestMoves[0] = true;
		bestMoves[1] = t.x;
		bestMoves[2] = t.y;
		goto deallocate;
	}

	for (uint16_t y = 0; y < gridHeight; y++)
	{
		for (uint16_t x = 0; x < gridWidth; x++)
		{
			float probability = probabilityMatrix[x + gridWidth * y];
			if (abs(probability) == highestProbability)
			{
				bestMoves[bestMovesSize] = (probability == abs(probability));
				bestMoves[bestMovesSize + 1] = x;
				bestMoves[bestMovesSize + 2] = y;
				bestMovesSize += 3;

				movesLimit--;
				if (!movesLimit)
				{
					goto deallocate;
				}
			}
		}
	}

deallocate:
	free(probabilityMatrix);
}
