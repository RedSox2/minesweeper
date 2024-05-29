import pygame
from classes import *

grid_interval = 50

Images.scale(grid_interval)

def draw_grid(window_w, window_h, color):
    block_size = grid_interval  # Set the size of the grid block
    for width in range(0, window_w, block_size):
        for height in range(0, window_h, block_size):
            rect = pygame.Rect(width, height, block_size, block_size)
            pygame.draw.rect(screen, color, rect, 1)

def iter_field(fld):
    return [(x_, y_, n) for x_, a_ in enumerate(fld) for y_, n in enumerate(a_)]

pygame.init()   

end_time = 0

X = Y = 22

center = (0, 0)

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

Grid.generateStartingGrid()
print(Grid.grid)
for row in Grid.grid:
    print(row)