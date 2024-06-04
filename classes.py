import random
import pygame

class Sound:
    def __init__(self, start: str, click: str, lose: str):
        self.start = pygame.mixer.Sound(start)
        self.click = pygame.mixer.Sound(click)
        self.lose = pygame.mixer.Sound(lose)

class GridSquare:
    def __init__(self, current, value):
        self.value = value
        self.current = current
        

    def __str__(self):
        return f"{self.current}, {self.value}"
        
    def getNeighbors(self, X, Y, x, y):
        self.neighbors = [(x2, y2) for x2 in range(x - 1, x + 2)
            for y2 in range(y - 1, y + 2)
            if (-1 < x <= X and
                -1 < y <= Y and
                (x != x2 or y != y2) and
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
                    gridRow.append(GridSquare(-2, -1))
                else:
                    gridRow.append(GridSquare(-2, -2))
            Grid.grid.append(gridRow)

        for row in range(1,21):
            for col in range(1,21):
                if (Grid.grid[row][col].value != -1):
                    Grid.grid[row][col].getNeighbors(Grid.size[0], Grid.size[1], col, row)
                    numMines = 0
                    for nx, ny in Grid.grid[row][col].neighbors:
                        if Grid.grid[ny][nx].value == -1:
                            numMines += 1
                    Grid.grid[row][col].value = numMines

    def addTopRow():
        if (Grid.center[1] > 1):
            Grid.center[1] -= 1
        else:
            Grid.size[1] += 1
            newRow = []
            row = 1
            for col in range(len(Grid.grid[-1])):
                if (random.random() <= Grid.density):
                    newRow.append(GridSquare(-2, -1))
                else:
                    newRow.append(GridSquare(-2, -2))

            Grid.grid.insert(0, newRow)

            for col in range(1, len(Grid.grid[-2])-1):
                if (Grid.grid[row][col].value != -1):
                        Grid.grid[row][col].getNeighbors(Grid.size[0], Grid.size[1], col, row)
                        numMines = 0
                        for nx, ny in Grid.grid[row][col].neighbors:
                            if Grid.grid[ny][nx].value == -1:
                                numMines += 1
                        Grid.grid[row][col].value = numMines

    
    def addBottomRow():

        if Grid.center[1]+20 < Grid.size[1]-2:
            Grid.center[1] += 1
        
        else:
            Grid.size[1] += 1
            Grid.center[1] += 1

            newRow = []
            row = len(Grid.grid)-1
            for col in range(len(Grid.grid[-1])):
                if (random.random() <= Grid.density):
                    newRow.append(GridSquare(-2, -1))
                else:
                    newRow.append(GridSquare(-2, -2))

            Grid.grid.append(newRow)

            for col in range(1, len(Grid.grid[-2])-1):
                if (Grid.grid[row][col].value != -1):
                        Grid.grid[row][col].getNeighbors(Grid.size[0], Grid.size[1], col, row)
                        numMines = 0
                        for nx, ny in Grid.grid[row][col].neighbors:
                            if Grid.grid[ny][nx].value == -1:
                                numMines += 1
                        Grid.grid[row][col].value = numMines
            print('')
             
        
    def addLeftRow():
        if Grid.center[0] > 1:
            Grid.center[0] -= 1
        else:
            Grid.size[0] += 1

            col = 1
            for row in range(len(Grid.grid)):
                if (random.random() <= Grid.density):
                    Grid.grid[row].insert(0, GridSquare(-2, -1))
                else:
                    Grid.grid[row].insert(0, GridSquare(-2, -2))
            
            for row in range(1, len(Grid.grid)-1):
                if (Grid.grid[row][col].value != -1):
                        Grid.grid[row][col].getNeighbors(Grid.size[0], Grid.size[1], col, row)
                        numMines = 0
                        for nx, ny in Grid.grid[row][col].neighbors:
                            if Grid.grid[ny][nx].value == -1:
                                numMines += 1
                        Grid.grid[row][col].value = numMines
            print('')


    def addRightRow():
        if Grid.center[0]+20 < Grid.size[0]-2:
            Grid.center[0] += 1
        else:
            Grid.size[0] += 1
            Grid.center[0] += 1

            col = len(Grid.grid[0])-1
            for row in range(len(Grid.grid)):
                if (random.random() <= Grid.density):
                    Grid.grid[row].append(GridSquare(-2, -1))
                else:
                    Grid.grid[row].append(GridSquare(-2, -2))
            
            for row in range(1, len(Grid.grid)-1):
                if (Grid.grid[row][col].value != -1):
                        Grid.grid[row][col].getNeighbors(Grid.size[0], Grid.size[1], col, row)
                        numMines = 0
                        for nx, ny in Grid.grid[row][col].neighbors:
                            if Grid.grid[ny][nx].value == -1:
                                numMines += 1
                        Grid.grid[row][col].value = numMines
            print('')

