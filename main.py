import pygame
from classes import *
from time import sleep
import os
import sys

grid_interval = 40


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def draw_grid(window_w, window_h, color):
    block_size = grid_interval  # Set the size of the grid block
    for width in range(0, window_w, block_size):
        for height in range(0, window_h, block_size):
            rect = pygame.Rect(width, height, block_size, block_size)
            pygame.draw.rect(screen, color, rect, 1)

def iter_field(fld):
    return [(x_, y_, n) for x_, a_ in enumerate(fld) for y_, n in enumerate(a_)]

seen = set()
def clearSquares(square: GridSquare, x, y):
    square.current = square.value
    seen.add(square)

    if not y > 1:
        Grid.addTopRow(override=True)
        Grid.center[1] += 1
    if not x > 1:
        Grid.addLeftRow(override=True)
        Grid.center[0] += 1
    if not y < Grid.size[1]-2:
        Grid.addBottomRow(override=True)
        Grid.center[1] -= 1
    if not x < Grid.size[0]-2:
        Grid.addRightRow(override=True)
        Grid.center[0] -= 1

    square.getNeighbors(Grid.size[0], Grid.size[1], x, y)
    for ncol, nrow in square.neighbors:
        
        if (neighborSquare := Grid.grid[nrow][ncol]).value == 0 and neighborSquare not in seen:
            clearSquares(neighborSquare, ncol, nrow)
            
        elif neighborSquare not in seen and neighborSquare.value != -1: 
            seen.add(neighborSquare)
            neighborSquare.current = neighborSquare.value
    return 

def openSquareParticles(particleSystem, event):
    topLeftX = event.pos[0]//grid_interval * grid_interval
    topLeftY = event.pos[1]//grid_interval * grid_interval
    for x in range(0,40):
        for y in range(0,40):
            if random.random() < 0.0125:
                particleSystem.create_collision_particles(pos=(topLeftX+x, topLeftY+y), randomness=0)


def lost():
    score = 0
    for row in range(len(Grid.grid)):
        for col, square in enumerate(Grid.grid[row]):
            if square.current == -3:
                if square.value == -1:
                    score += 2
                else:
                    score -= 10
            elif square.current != -2:
                score += (square.current+1) ** 1.55
    intScore = round(score)
    print(f"Your score was: {intScore}")

    score = time_font.render(f"Your score was: {intScore}", True, lose_color)
    score_rect = score.get_rect()
    score_rect.center = (window_width // 2, window_height // 2)

    for row in range(0+Grid.center[1],20+Grid.center[1]):
        for col in range(0+Grid.center[0],20+Grid.center[0]):
            if Grid.grid[row][col].value == -1:
                screen.blit(Images.squares[-1], ((col-Grid.center[0])*grid_interval, (row-Grid.center[1])*grid_interval))
            else:
                screen.blit(Images.squares[Grid.grid[row][col].current], ((col-Grid.center[0])*grid_interval, (row-Grid.center[1])*grid_interval))

    screen.blit(lose, lose_rect)
    screen.blit(score, score_rect)
    pygame.display.update()
    sound.lose.play()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_grid(grid_interval*X, grid_interval*Y, grey_grid)
        for row in range(0+Grid.center[1],20+Grid.center[1]):
            for col in range(0+Grid.center[0],20+Grid.center[0]):
                if Grid.grid[row][col].value == -1:
                    screen.blit(Images.squares[-1], ((col-Grid.center[0])*grid_interval, (row-Grid.center[1])*grid_interval))
                else:
                    screen.blit(Images.squares[Grid.grid[row][col].current], ((col-Grid.center[0])*grid_interval, (row-Grid.center[1])*grid_interval))
        particlesMine1.update(1/60)
        particlesMine2.update(1/60)
        particlesNormal.update(1/60)
        screen.blit(lose, lose_rect)
        screen.blit(score, score_rect)
        clock.tick(60)
        pygame.display.update()

pygame.init()

end_time = 0

X = Y = 20

window_width = X*grid_interval
window_height = Y*grid_interval

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("MINESWEEPER")
clock = pygame.time.Clock()

sound = Sound(resource_path("open.wav"), resource_path("open_many.wav"), resource_path("lose.wav"), resource_path("flag.wav"))
font_size = 350*window_height//1440
font = pygame.font.Font(resource_path("8bit.ttf"), font_size)
time_font = pygame.font.Font(resource_path("8bit.ttf"), font_size//3)

lose_color = (200, 0, 0)

lose = font.render("The End!", True, lose_color)

lose_rect = lose.get_rect()

lose_rect.center = (window_width // 2, window_height // 3)

grey_grid = (128, 128, 128)

particlesNormal = ParticleSystem(screen, lifetime=1, start_color=(138, 138, 138), end_color=(138, 138, 138), start_radius=5, particle_count=1, speed=75, acc=(0, 0))
particlesMine1 = ParticleSystem(screen, lifetime=6, start_color=(230, 0, 0), end_color=(138, 138, 138), start_radius=10, particle_count=200, speed=300, acc=(0, 100))
particlesMine2 = ParticleSystem(screen, lifetime=6, start_color=(230, 165, 0), end_color=(138, 138, 138), start_radius=10, particle_count=200, speed=300, acc=(0, 100))

class Images:
    
    squares = [

        pygame.image.load(resource_path('open.jpg')),
        pygame.image.load(resource_path('1.jpg')),
        pygame.image.load(resource_path('2.jpg')),
        pygame.image.load(resource_path('3.jpg')),
        pygame.image.load(resource_path('4.jpg')),
        pygame.image.load(resource_path('5.jpg')),
        pygame.image.load(resource_path('6.jpg')),
        pygame.image.load(resource_path('7.jpg')),
        pygame.image.load(resource_path('8.jpg')),

        pygame.image.load(resource_path('flag.jpg')),
        pygame.image.load(resource_path('unopened.jpg')),
        pygame.image.load(resource_path('mine.jpg'))

        ]
    
    def scale(grid_interval):
        for i in range(len(Images.squares)):
            Images.squares[i] = pygame.transform.scale(Images.squares[i], (grid_interval, grid_interval))

Images.scale(grid_interval-1)

Grid.generateStartingGrid(0.2)

draw_grid(grid_interval*X, grid_interval*Y, grey_grid)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                Grid.addTopRow()
            if event.key == pygame.K_a:
                Grid.addLeftRow()
            if event.key == pygame.K_s:
                Grid.addBottomRow()
            if event.key == pygame.K_d:
                Grid.addRightRow()

        if event.type == pygame.MOUSEBUTTONDOWN:
            selectedCol = event.pos[0]//grid_interval + Grid.center[0]
            selectedRow = event.pos[1]//grid_interval + Grid.center[1]
            
            if event.button == 1:
                if (selectedSquare := Grid.grid[selectedRow][selectedCol]).current == -2:
                    if selectedSquare.value == 0:
                        sound.open_many.play()
                        clearSquares(selectedSquare, selectedCol, selectedRow)
                        openSquareParticles(particlesNormal, event)
                    elif selectedSquare.value == -1: 
                        particlesMine1.create_collision_particles(pos=(event.pos[0], event.pos[1]), randomness=50)
                        particlesMine2.create_collision_particles(pos=(event.pos[0], event.pos[1]), randomness=50)
                        lost()  
                    else:
                        sound.open.play()
                        selectedSquare.current = Grid.grid[selectedRow][selectedCol].value
                        openSquareParticles(particlesNormal, event)
                

            elif event.button == 3:
                sound.flag.play()
                if (selectedSquare := Grid.grid[selectedRow][selectedCol]).current == -3:
                    selectedSquare.current = -2
                elif (selectedSquare.current == -2):
                    selectedSquare.current = -3

    draw_grid(grid_interval*X, grid_interval*Y, grey_grid)
    for row in range(0+Grid.center[1],20+Grid.center[1]):
        for col in range(0+Grid.center[0],20+Grid.center[0]):
            screen.blit(Images.squares[Grid.grid[row][col].current], ((col-Grid.center[0])*grid_interval, (row-Grid.center[1])*grid_interval))
    #particles.create_collision_particles(pos=(200, 200))
    particlesNormal.update(1/60)
    pygame.display.update()
    clock.tick(60)
