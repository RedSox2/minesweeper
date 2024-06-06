import math
import pygame
from classes import *
#from cryptography.fernet import Fernet
from datetime import datetime
from time import sleep

grid_interval = 40

#f = Fernet('nIdceQJdk0GCuhLi31hP8k_K00MtIwveEHszdpM1I24='.encode())


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

    if not y > 2:
        Grid.addTopRow()
        Grid.center[1] += 1
    if not x > 2:
        Grid.addLeftRow()
        Grid.center[0] += 1
    if not y < Grid.size[1]-3:
        Grid.addBottomRow()
        Grid.center[1] -= 1
    if not x < Grid.size[0]-3:
        Grid.addRightRow()
        Grid.center[0] -= 1

    square.getNeighbors(Grid.size[0], Grid.size[1], x, y)
    for ncol, nrow in square.neighbors:
        
        if (neighborSquare := Grid.grid[nrow][ncol]).value == 0 and neighborSquare not in seen:
            seen.add(neighborSquare)
            clearSquares(neighborSquare, seen, ncol, nrow)
            
        elif neighborSquare not in seen and neighborSquare.value != -1: 
            seen.add(neighborSquare)
            neighborSquare.current = neighborSquare.value
    return 


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
                score += square.current ** 1.55
    intScore = round(score)
    print(f"Your score was: {intScore}")

    '''with open('highscore.txt', 'r') as file:
        data = file.read().encode()
    prevHighScore = int(f.decrypt(data).decode().split()[-1])'''

                
    

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
    '''if intScore > prevHighScore:
        print("You got a highscore!")
        name = input('Please enter your name for the record: ')
        date = str(datetime.now())

        toWrite = f'Name: {name}\nDate: {date}\nScore: {intScore}'.encode()
        with open('highscore.txt', 'w') as file:
            file.write(f.encrypt(toWrite).decode())'''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        draw_grid(grid_interval*X, grid_interval*Y, grey_grid)
        for row in range(0+Grid.center[1],20+Grid.center[1]):
            for col in range(0+Grid.center[0],20+Grid.center[0]):
                if Grid.grid[row][col].value == -1:
                    screen.blit(Images.squares[-1], ((col-Grid.center[0])*grid_interval, (row-Grid.center[1])*grid_interval))
                else:
                    screen.blit(Images.squares[Grid.grid[row][col].current], ((col-Grid.center[0])*grid_interval, (row-Grid.center[1])*grid_interval))
        particles.update(1/60)
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

sound = Sound("open.wav", "open_many.wav", "lose.wav", "flag.wav")
font_size = 350*window_height//1440
font = pygame.font.Font("8bit.ttf", font_size)
time_font = pygame.font.Font("8bit.ttf", font_size//3)

lose_color = (200, 0, 0)

lose = font.render("The End!", True, lose_color)

lose_rect = lose.get_rect()

lose_rect.center = (window_width // 2, window_height // 3)

grey_grid = (128, 128, 128)

particles = ParticleSystem(screen, lifetime=2, start_color=(138, 138, 138), end_color=(138, 138, 138), start_radius=5, particle_count=20, speed=40, acc=(0, 20))

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

Grid.generateStartingGrid(0.2)

draw_grid(grid_interval*X, grid_interval*Y, grey_grid)


'''with open('highscore.txt', 'r') as file:
    highscore = file.read().encode()
    highscore = f.decrypt(highscore).decode()
    print("The current highscore is:")
    print(highscore)
    sleep(5)'''

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
                        sound.open_many.play()
                        clearSquares(selectedSquare, set(), selectedCol, selectedRow)
                        particles.create_collision_particles(pos=(event.pos[0], event.pos[1]))
                    elif selectedSquare.value == -1: 
                        particles.create_collision_particles(pos=(event.pos[0], event.pos[1]))
                        lost()  
                    else:
                        sound.open.play()
                        selectedSquare.current = Grid.grid[selectedRow][selectedCol].value
                        particles.create_collision_particles(pos=(event.pos[0], event.pos[1]))
                

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
    particles.update(1/60)
    pygame.display.update()
    clock.tick(60)
