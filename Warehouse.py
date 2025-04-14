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
        self.robot = robot
        for i in range(grid_size):
            self.grid.append([])
            for j in range(grid_size):
                c = Cell(i, j)
                self.grid[i].append(c)

        self.delivery_points = set() 
        self.delivered_boxes = []

    def add_box(self, x, y,box):
        self.grid[x][y].box = box

    def add_delivery_point(self, x, y):
        self.delivery_points.add((x,y))

    def draw(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                cell = self.grid[i][j]
                rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect, 1)

                if i == self.robot.x and j == self.robot.y:
                    pygame.draw.circle(screen, RED, (i*CELL_SIZE + CELL_SIZE/2, j*CELL_SIZE+ CELL_SIZE/2,), CELL_SIZE/3) # green border

                if cell.shelf is not None:
                    rect = pygame.Rect(i * CELL_SIZE + 10, j * CELL_SIZE + 10, CELL_SIZE - 20, CELL_SIZE - 20)
                    pygame.draw.rect(screen, GRAY, rect)  # yellow box

                # Highlight delivery points
                if (i, j) in self.delivery_points:
                    rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, GREEN, rect, 3)  # green border

                # Highlight delivered boxes
                if (i, j) in self.delivered_boxes:
                    rect = pygame.Rect(i * CELL_SIZE + 10, j * CELL_SIZE + 10, CELL_SIZE - 20, CELL_SIZE - 20)
                    pygame.draw.rect(screen, YELLOW, rect)  # yellow box