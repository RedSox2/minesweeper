import pygame

class Images:
    unopened = pygame.image.load("unopened.jpg")
    flag = pygame.image.load("flag.jpg")
    mine = pygame.image.load("mine.jpg")
    squares = [
        pygame.image.load("open.jpg"),
        pygame.image.load('1.jpg'),
        pygame.image.load('2.jpg'),
        pygame.image.load('3.jpg'),
        pygame.image.load('4.jpg'),
        pygame.image.load('5.jpg'),
        pygame.image.load('6.jpg'),
        pygame.image.load('7.jpg'),
        pygame.image.load('8.jpg')
    ]
    
    def scale(grid_interval):
        unopened = pygame.transform.scale(unopened, (grid_interval, grid_interval))
        flag = pygame.transform.scale(flag, (grid_interval, grid_interval))
        mine = pygame.transform.scale(mine, (grid_interval, grid_interval))
        for i in range(len(squares)):
            squares[i] = pygame.transform.scale(squares[i], (grid_interval, grid_interval))

class GridSquare:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        
    def getNeighbors(self, X, Y):
        self.neighbors = [(x2, y2) for x2 in range(self.x - 1, self.x + 2)
            for y2 in range(self.y - 1, self.y + 2)
            if (-1 < self.x <= X and
                -1 < self.y <= Y and
                (self.x != x2 or self.y != y2) and
                (-1 < x2 < X) and
                (-1 < y2 < Y))]