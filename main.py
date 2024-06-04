import pygame
from classes import *

grid_interval = 40

def draw_grid(window_w, window_h, color):
    block_size = grid_interval  # Set the size of the grid block
    for width in range(0, window_w, block_size):
        for height in range(0, window_h, block_size):
            rect = pygame.Rect(width, height, block_size, block_size)
            pygame.draw.rect(screen, color, rect, 1)

def iter_field(fld):
    return [(x_, y_, n) for x_, a_ in enumerate(fld) for y_, n in enumerate(a_)]

def clearSquares(square: GridSquare, seen: set[GridSquare], x, y):
    square.current = square.value
    seen = set(seen)
    seen.add(square)
    square.getNeighbors(Grid.size[0], Grid.size[1], x, y)
    for ncol, nrow in square.neighbors:
        
        if (neighborSquare := Grid.grid[nrow][ncol]).value == 0 and neighborSquare not in seen:
            seen.add(neighborSquare)
            clearSquares(neighborSquare, seen, ncol, nrow)
        else: 
            seen.add(neighborSquare := Grid.grid[nrow][ncol])
            print("clearing")
            neighborSquare.current = neighborSquare.value
    return 

pygame.init()

end_time = 0

X = Y = 20

window_width = X*grid_interval
window_height = Y*grid_interval

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("MINESWEEPER")

font_size = 350*window_height//1440
font = pygame.font.Font("8bit.ttf", font_size)
time_font = pygame.font.Font("8bit.ttf", font_size//3)

win_color = (255, 255, 255)
lose_color = (255, 0, 0)

win = font.render("You Win :D", False, win_color)
lose = font.render("You Lost :(", False, lose_color)

win_rect = win.get_rect()
lose_rect = lose.get_rect()

win_rect.center = lose_rect.center = (window_width // 2, window_height // 2)

grey_grid = (128, 128, 128)


class Images:
    
    squares = [

        pygame.image.load("open.jpg"),
        pygame.image.load('1.jpg'),
        pygame.image.load('2.jpg'),
        pygame.image.load('3.jpg'),
        pygame.image.load('4.jpg'),
        pygame.image.load('5.jpg'),
        pygame.image.load('6.jpg'),
        pygame.image.load('7.jpg'),
        pygame.image.load('8.jpg'),

        pygame.image.load("flag.jpg"),
        pygame.image.load("unopened.jpg"),
        pygame.image.load("mine.jpg")

        ]
    
    def scale(grid_interval):
        for i in range(len(Images.squares)):
            Images.squares[i] = pygame.transform.scale(Images.squares[i], (grid_interval, grid_interval))

Images.scale(grid_interval-1)

Grid.generateStartingGrid(.2)

draw_grid(grid_interval*X, grid_interval*Y, grey_grid)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                Grid.addTopRow()
            if event.key == pygame.K_a:
                Grid.addLeftRow()
            if event.key == pygame.K_s:
                # print("typed")

                Grid.addBottomRow()
            if event.key == pygame.K_d:
                Grid.addRightRow()

        if event.type == pygame.MOUSEBUTTONDOWN:
            selectedCol = event.pos[0]//grid_interval + Grid.center[0]
            selectedRow = event.pos[1]//grid_interval + Grid.center[1]
            
            if event.button == 1:
                if (selectedSquare := Grid.grid[selectedRow][selectedCol]).current == -2:
                    if selectedSquare.value == 0:
                        clearSquares(selectedSquare, set(), selectedCol, selectedRow)
                    else:
                        selectedSquare.current = Grid.grid[selectedRow][selectedCol].value

            elif event.button == 3:
                if (selectedSquare := Grid.grid[selectedRow][selectedCol]).current == -3:
                    selectedSquare.current = -2
                else: 
                    selectedSquare.current = -3

    for row in range(0+Grid.center[1],20+Grid.center[1]):
        for col in range(0+Grid.center[0],20+Grid.center[0]):
            screen.blit(Images.squares[Grid.grid[row][col].current], ((col-Grid.center[0])*grid_interval, (row-Grid.center[1])*grid_interval))

    pygame.display.update()
