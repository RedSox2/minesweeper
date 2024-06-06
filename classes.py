import math
import random
import pygame

class Sound:
    def __init__(self, open, open_many, lose,  flag):
        self.open = pygame.mixer.Sound(open)
        self.open_many = pygame.mixer.Sound(open_many)
        self.flag = pygame.mixer.Sound(flag)
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

class ParticleSystem:
    def __init__(self, screen, *, lifetime, vel=(0, 0), start_color, end_color, start_radius, end_radius=0, border_width=0,
                 particle_count=0, acc=(0, 0), speed=0):
        self.particles = []
        self.lifetime = lifetime
        self.vel = vel
        self.start_color = start_color
        self.end_color = end_color
        self.start_radius = start_radius
        self.end_radius = end_radius
        self.border_width = border_width
        self.particle_count = particle_count
        self.acc = acc
        self.speed = speed
        self.screen = screen

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.remove_dead_particles()

    def remove_dead_particles(self):
        alive_particles = []
        for particle in self.particles:
            if particle.is_alive():
                alive_particles.append(particle)
        self.particles = alive_particles

    def create_trail_particles(self, *, pos):
        self.particles.append(Particle(pos=pos, lifetime=self.lifetime, vel=self.vel, start_color=self.start_color,
                                       end_color=self.end_color,
                                       start_radius=self.start_radius, end_radius=self.end_radius,
                                       border_width=self.border_width))

    def create_collision_particles(self, *, pos):
        for i in range(0, self.particle_count):
            angle = random.random() * math.tau
            random_vel = (math.cos(angle) * (random.random() * self.speed), math.sin(angle) * (random.random() * self.speed))

            self.particles.append(
                Particle(self.screen, pos=pos, lifetime=self.lifetime, vel=random_vel, acc=self.acc, start_color=self.start_color,
                         end_color=self.end_color, start_radius=self.start_radius, end_radius=self.end_radius,
                         border_width=self.border_width))



class Particle:
    def __init__(self, screen, *, lifetime, pos, vel, acc=(0, 0), start_color, end_color, start_radius, end_radius=0,
                 border_width=0):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.acc = pygame.Vector2(acc)

        self.color = start_color

        self.radius = start_radius
        self.radius_change = (end_radius - start_radius) / lifetime

        self.border_width = border_width
        self.lifetime = lifetime
        self.screen = screen

    def update(self, dt):
        self.move(dt)
        self.shrink(dt)
        self.fade(dt)
        self.draw()
        self.update_time(dt)

    def move(self, dt):
        self.pos += self.vel * dt
        self.vel += self.acc * dt

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius, self.border_width)

    def shrink(self, dt):
        self.radius += self.radius_change * dt
        if self.radius < 0:
            self.radius = 0

    def fade(self, dt):
        #self.color += self.color_change * dt
        #self.color.keep_within_bounds()
        pass

    def update_time(self, dt):
        self.lifetime -= dt

    def is_alive(self):
        return self.lifetime > 0
