WIDTH, HEIGHT = 1200, 600
CELL_SIZE = 50
ROWS, COLUMNS = HEIGHT // CELL_SIZE, (WIDTH - 150) // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
SHELF_COLOR = (120, 120, 120)

import pygame

class Box:
    def __init__(self, s):
        self.name = s


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.box = None


class Warehouse:
    def __init__(self, grid_size, robot):
        self.grid = []
        self.grid_size = grid_size
        self.robot = robot
        for i in range(grid_size):
            self.grid.append([])
            for j in range(grid_size):
                c = Cell(i, j)
                self.grid[i].append(c)


    def add_box(self, x, y,box):
        self.grid[x][y].box = box


    def draw(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                cell = self.grid[i][j]
                rect = pygame.Rect(i * CELL_SIZE,  j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)

                if i == self.robot.x and j == self.robot.y:
                    if self.robot.rotation == "N": rotation_offset = (0, 1)
                    elif self.robot.rotation == "E": rotation_offset = (1, 0)
                    elif self.robot.rotation == "S": rotation_offset = (0, -1)
                    else: rotation_offset = (-1, 0)

                    pygame.draw.circle(screen, RED, (i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE+ CELL_SIZE/2,), CELL_SIZE/3)
                    pygame.draw.circle(screen, WHITE, (i*CELL_SIZE + CELL_SIZE/2 + rotation_offset[0]*10, j*CELL_SIZE+ CELL_SIZE/2+ rotation_offset[1]*10,), CELL_SIZE/7)

                if cell.box is not None:
                    rect = pygame.Rect(i * CELL_SIZE + 10, j * CELL_SIZE + 10, CELL_SIZE - 20, CELL_SIZE - 20)
                    pygame.draw.rect(screen, YELLOW, rect)  # yellow box
