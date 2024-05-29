import pygame
from random import seed, randint

grid_interval = 50


def draw_grid(window_w, window_h, color):
    block_size = grid_interval  # Set the size of the grid block
    for width in range(0, window_w, block_size):
        for height in range(0, window_h, block_size):
            rect = pygame.Rect(width, height, block_size, block_size)
            pygame.draw.rect(screen, color, rect, 1)


def neighbors(x_, y_):
    return [(x2, y2) for x2 in range(x_ - 1, x_ + 2)
            for y2 in range(y_ - 1, y_ + 2)
            if (-1 < x_ <= X and
                -1 < y_ <= Y and
                (x_ != x2 or y_ != y2) and
                (-1 < x2 < X) and
                (-1 < y2 < Y))]


# returns flattened tuples of the x and y indices and the n value
def iter_field(fld):
    return [(x_, y_, n) for x_, a_ in enumerate(fld) for y_, n in enumerate(a_)]


X = int(input("How big will the board be: "))
X = 6 if X < 6 else X
if X > 28:
    grid_interval = 1400 // X

Y = X

mines_num = int(input("How many mines will there be: "))
mines_num = [mines_num, 1][mines_num < 1]
if mines_num > (X**2)-9:
    mines_num = X**2-9

pygame.init()

end_time = 0

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


class Images:
    unopened = pygame.image.load("unopened.jpg")
    unopened = pygame.transform.scale(unopened, (grid_interval, grid_interval))
    flag = pygame.image.load("flag.jpg")
    flag = pygame.transform.scale(flag, (grid_interval, grid_interval))
    mine = pygame.image.load("mine.jpg")
    mine = pygame.transform.scale(mine, (grid_interval, grid_interval))
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
    for i in range(len(squares)):
        squares[i] = pygame.transform.scale(squares[i], (grid_interval, grid_interval))


grey_grid = (128, 128, 128)

chosen = []

field = []
shown = []
for i in range(X):
    field.append(["u" for _ in range(Y)])
    shown.append([Images.unopened for n in range(Y)])

set_open = True
failed = False
done = False
won = False
check_x = None
check_y = None

while 1:

    if failed:
        if not done:
            print("You failed!")
        done = True
        for x, y, n in iter_field(field):
            if n == "m":
                check_x = x
                check_y = y
                shown[x][y] = Images.mine

    while any([shown[nx][ny] == Images.unopened for x, y, n in iter_field(shown) for nx, ny in neighbors(x, y)
               if n == Images.squares[0]]):
        for x, y, n in iter_field(shown):
            if n == Images.squares[0]:
                for sx, sy in neighbors(x, y):
                    shown[sx][sy] = Images.squares[field[sx][sy]]
    for x, y, n in iter_field(shown):
        screen.blit(n, (x*grid_interval, y*grid_interval))

    draw_grid(window_width, window_height, grey_grid)

    if won:
        your_time = time_font.render(f"Your time was: {end_time}", False, win_color)
        your_time_rect = your_time.get_rect()
        your_time_rect.center = (window_width // 2, win_rect.bottom + (font_size//3))
        screen.blit(win, win_rect)
        screen.blit(your_time, your_time_rect)
    if failed:
        screen.blit(lose, lose_rect)

    pygame.display.update()

    if all(shown[x][y] != Images.unopened and shown[x][y] != Images.flag for x, y, n in iter_field(field) if n != "m") \
            and not won:
        end_time = (pygame.time.get_ticks() - begin_time) / 1000
        print(f"Your time was: {end_time} seconds!")
        won = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and not won and not failed:
            sel_x = event.pos[0]//grid_interval
            sel_y = event.pos[1]//grid_interval
            if set_open:
                begin_time = pygame.time.get_ticks()
                set_open = False
                chosen.append((sel_x, sel_y))
                for x, y in neighbors(sel_x, sel_y):
                    chosen.append((x, y))
                shown[sel_x][sel_y] = Images.squares[0]
                mines = []
                for i in range(mines_num):
                    while 1:
                        seed()
                        coord = (randint(0, X-1), randint(0, Y-1))
                        if coord not in chosen:
                            mines.append(coord)
                            chosen.append(coord)
                            break
                for a, b in mines:
                    field[a][b] = "m"
                for x, y, i in iter_field(field):
                    if i != "m":
                        mine_num = sum(field[xc][yc] == "m" for xc, yc in neighbors(x, y))
                        field[x][y] = mine_num
            else:
                if event.button == 1:
                    if shown[sel_x][sel_y] != Images.flag:
                        if field[sel_x][sel_y] == "m":
                            failed = True
                        elif shown[sel_x][sel_y] != Images.unopened:
                            for x, y in neighbors(sel_x, sel_y):
                                if field[x][y] == "m" and shown[x][y] != Images.flag:
                                    failed = True
                                elif shown[x][y] != Images.flag:
                                    shown[x][y] = Images.squares[field[x][y]]
                        else:
                            shown[sel_x][sel_y] = Images.squares[field[sel_x][sel_y]]
                elif event.button == 3 and shown[sel_x][sel_y] == Images.unopened or shown[sel_x][sel_y] == Images.flag:
                    shown[sel_x][sel_y] = [Images.flag, Images.unopened][shown[sel_x][sel_y] == Images.flag]
