class Box:
    def __init__(self, s):
        self.name = s


class Shelf:
    def __init__(self):
        self.boxes = []

    def add_box(self, box):
        self.boxes.append(box)


class Cell:
    def __init__(self, pos):
        self.pos = pos
        self.shelf = None


class Warehouse:
    def __init__(self, grid_size):
        self.grid = []
        for i in range(grid_size):
            self.grid.append([])
            for j in range(grid_size):
                c = Cell((i, j))
                self.grid[i].append(c)

        print(self.grid[4][1].pos)

    def add_shelf(self, pos,shelf):
        self.grid[pos[0]][pos[1]].shelf = shelf

