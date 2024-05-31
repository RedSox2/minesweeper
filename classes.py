import pygame
import random

class GridSquare:
    def __init__(self, current, value, x, y):
        self.value = value
        self.current = current
        self.x = x
        self.y = y
        

    def __str__(self):
        return f"{self.current}, {self.value}, {self.x}, {self.y}"
        
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
    size = [22, 22]
    center = [1, 1]


    def generateStartingGrid(density=0.2):
        Grid.density = density
        for row in range(Grid.size[1]):
            gridRow = []
            for col in range(Grid.size[0]):
                if (random.random() < density):
                    # -1 == mine, -2 == unopened
                    gridRow.append(GridSquare(-2, -1, col, row))
                else:
                    gridRow.append(GridSquare(-2, -2, col, row))
            Grid.grid.append(gridRow)

        for row in range(1,21):
            for col in range(1,21):
                if (Grid.grid[row][col].value != -1):
                    Grid.grid[row][col].getNeighbors(Grid.size[0], Grid.size[1])
                    numMines = 0
                    for nx, ny in Grid.grid[row][col].neighbors:
                        if Grid.grid[nx][ny].value == -1:
                            numMines += 1
                    Grid.grid[row][col].value = numMines

    def addTopRow():
        pass
    
    def addBottomRow():
        
        newRow = []
        row = len(Grid.grid)
        for col in range(len(Grid.grid[-1])):
            if (random.random() <= Grid.density):
                newRow.append(GridSquare(-2, -1, col, row))
            else:
                newRow.append(GridSquare(-2, -2, col, row))

        Grid.grid.append(newRow)

        for col in range(len(Grid.grid[-2])):
            if (Grid.grid[row][col].value != -1):
                    Grid.grid[row][col].getNeighbors(Grid.size[0], Grid.size[1])
                    numMines = 0
                    for nx, ny in Grid.grid[row][col].neighbors:
                        if Grid.grid[nx][ny].value == -1:
                            numMines += 1
                    Grid.grid[row][col].value = numMines
        Grid.center[1] += 1
            
        
        


    def addLeftRow():
        pass

    def addRightRow():
        pass

    