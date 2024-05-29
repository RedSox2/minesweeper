import pygame
import random

class GridSquare:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.value}, {self.x}, {self.y}"
        
    def getNeighbors(self, X, Y):
        self.neighbors = [(x2, y2) for x2 in range(self.x - 1, self.x + 2)
            for y2 in range(self.y - 1, self.y + 2)
            if (-1 < self.x <= X and
                -1 < self.y <= Y and
                (self.x != x2 or self.y != y2) and
                (-1 < x2 < X) and
                (-1 < y2 < Y))]
        
class Grid:
    grid = []

    def generateStartingGrid(density=0.2):
        for row in range(22):
            gridRow = []
            for col in range(22):
                if (random.random() < density):
                    #-1 == mine
                    gridRow.append(GridSquare(-1, row, col))
                else:
                    gridRow.append(GridSquare(0, row, col))
            Grid.grid.append(gridRow)

        for row in range(1,21):
            for col in range(1,21):
                if (Grid.grid[row][col].value != -1):
                    Grid.grid[row][col].getNeighbors(22, 22)
                    numMines = 0
                    for nx, ny in Grid.grid[row][col].neighbors:
                        if Grid.grid[nx][ny].value == -1:
                            numMines += 1
                    Grid.grid[row][col].value = numMines

    def addTopRow():
        pass
    
    def addBottomRow():
        pass

    def addLeftRow():
        pass

    def addRightRow():
        pass

    