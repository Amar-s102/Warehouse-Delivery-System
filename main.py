import pygame
from Warehouse import *
from Robot import *

# --- Constants ---
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 50
ROWS, COLUMNS = HEIGHT // CELL_SIZE, (WIDTH - 150) // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SHELF_COLOR = (120, 120, 120)

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Warehouse Delivery System")
CLOCK = pygame.time.Clock()
FPS = 30

# --- Classes ---
class Button:
    def __init__(self, x, y, width, height, text, color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)
        font = pygame.font.SysFont(None, 32)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        SCREEN.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# --- Setup ---
robot = Robot(0, 0)
warehouse = Warehouse(12, robot)
warehouse.add_box(1, 3, Box("batata"))
warehouse.add_box(7, 4, Box("batat1"))
warehouse.add_box(3, 6, Box("batat2"))
warehouse.add_box(4, 9, Box("batat3"))
warehouse.add_box(1, 2, Box("batat4"))

# robot.go_to_position(1, 1, warehouse)
# --- Main Loop ---
def main():
    running = True
    while running:
        CLOCK.tick(FPS)
        SCREEN.fill(BLACK)

        if len(robot.actions) > 0:
            robot.update_movement(warehouse)
        # else:
        #     robot.pickup_box(warehouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x, y = mx // CELL_SIZE, my // CELL_SIZE
                if pygame.mouse.get_pressed()[0] and len(robot.actions) == 0:
                    if warehouse.grid[x][y].box is not None and robot.c is None:
                        robot.go_to_box(x, y,warehouse, True)
                    elif warehouse.grid[x][y].box is None and robot.c is not None:
                        robot.go_to_box(x, y, warehouse, False)
                    elif warehouse.grid[x][y].box is None:
                        robot.go_to_position(x, y, warehouse)
                elif pygame.mouse.get_pressed()[2]:
                    warehouse.add_box(x, y, Box("batata"))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    robot.move_forward(warehouse)
                if event.key == pygame.K_d:
                    robot.rotate_right(warehouse)
                if event.key == pygame.K_s:
                    robot.move_backward(warehouse)
                if event.key == pygame.K_a:
                    robot.rotate_left(warehouse)
                if event.key == pygame.K_p:
                    robot.pickup_box(warehouse)



        warehouse.draw(SCREEN)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
