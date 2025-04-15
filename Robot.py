import math
from Warehouse import *

class Robot:
    def __init__(self, x,y):
        self.x=x
        self.y=y
        self.rotation= 'E'
        self.c=None
        self.move_cost=0
        self.actions = []


    def findTargetRotation(self, x1, y1, x2, y2):
        if x1 < x2:
            return 'E'
        elif x1 > x2:
            return 'W'
        elif y1 < y2:
            return 'N'
        else:
            return 'S'

    def calculateRotationCost(self, current_rotation, target_rotation):
        rotations = ['N', 'E', 'S', 'W']
        current_index = rotations.index(current_rotation)
        target_index = rotations.index(target_rotation)
        rotation_cost = min(abs(current_index - target_index), 4 - abs(current_index - target_index))
        return rotation_cost

    def heuristic(self, x1, y1, x2, y2, current_rotation, optional_rot = None):
        distance_cost = abs(x1 - x2) + abs(y1 - y2)

        target_rotation = self.findTargetRotation(x1, y1, x2, y2)

        rotation_cost = self.calculateRotationCost(current_rotation, target_rotation)

        if optional_rot is not None:
            rotation_cost += self.calculateRotationCost(target_rotation, optional_rot)

        return distance_cost + rotation_cost

    

    def find_path(self,warehouse,target_x,target_y):
        open_set=[]
        img_x, img_y= self.x, self.y
        img_rotation = self.rotation
        img_cost = 0
        path = []
        while img_x != target_x or img_y != target_y:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x = img_x + dx
                new_y = img_y + dy
                new_rotation = self.findTargetRotation(img_x, img_y, new_x, new_y)
                if self.valid_move(warehouse, new_x, new_y) and not path.__contains__((new_x, new_y)):
                    new_path = path.copy()
                    new_path.append((new_x, new_y))
                    actual_cost = img_cost + 1 + self.calculateRotationCost(img_rotation, new_rotation)
                    cost = self.heuristic(new_x, new_y, target_x, target_y, img_rotation) + actual_cost
                    open_set.append((cost, actual_cost, new_x, new_y, new_rotation, new_path))
                    open_set.sort(key=lambda x: x[0]) 

            img_cost = open_set[0][1]
            img_x = open_set[0][2]
            img_y = open_set[0][3]
            img_rotation = open_set[0][4]
            path = open_set[0][5]
            open_set.remove(open_set[0])
        
        return path

            
    def go_to_position(self, x, y, warehouse):
        path = self.find_path(warehouse, x, y)
        rotations = ['N', 'E', 'S', 'W']
        self.actions = []
        sim_robot = Robot(self.x, self.y)
        sim_robot.rotation = self.rotation
        for pos in path:
            target_rotation = self.findTargetRotation(sim_robot.x, sim_robot.y, pos[0], pos[1])
            current_index = rotations.index(sim_robot.rotation)
            target_index = rotations.index(target_rotation)
            rotation_degree = (target_index - current_index) % 4
            if rotation_degree == 0:
                sim_robot.move_forward(warehouse)
                self.actions.append(0)
            elif rotation_degree == 1:
                sim_robot.rotate_right(warehouse)
                sim_robot.move_forward(warehouse)
                self.actions.append(1)
                self.actions.append(0)
            elif rotation_degree == 3:
                sim_robot.rotate_left(warehouse)
                sim_robot.move_forward(warehouse)
                self.actions.append(2)
                self.actions.append(0)
            else:
                sim_robot.move_backward(warehouse)
                self.actions.append(3)

        return sim_robot.rotation

    def go_to_box(self, x, y,warehouse, pickup):
        minimum_cost = math.inf
        best_cell = None
        target_rot = None
        rotation_dict = {(0, 1) : 'S', (1, 0) : 'W', (0, -1): 'N', (-1, 0) : 'E'}
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x = x + dx
            new_y = y + dy
            if self.valid_move(warehouse, new_x, new_y):
                new_cost = self.heuristic(self.x, self.y, new_x, new_y, self.rotation, rotation_dict[(dx, dy)])
                if new_cost < minimum_cost:
                    minimum_cost = new_cost
                    best_cell = warehouse.grid[new_x][new_y]
                    target_rot = rotation_dict[(dx, dy)]

        if best_cell is not None:
            current_rotation = self.go_to_position(best_cell.x, best_cell.y, warehouse)

            rotations = ['N', 'E', 'S', 'W']
            current_index = rotations.index(current_rotation)
            target_index = rotations.index(target_rot)
            rotation_diff = (target_index - current_index) % 4

            print(target_rot)

            if rotation_diff == 1:
                self.actions.append(1)
            elif rotation_diff == 2:
                self.actions.append(1)
                self.actions.append(1)
            elif rotation_diff == 3:
                self.actions.append(2)

            if pickup:
                self.actions.append(4)
            else:
                self.actions.append(5)

    def update_movement(self, warehouse):
        action = self.actions.pop(0)
        if action == 0:
            self.move_forward(warehouse)
        elif action == 1:
            self.rotate_right(warehouse)
        elif action == 2:
            self.rotate_left(warehouse)
        elif action == 3:
            self.move_backward(warehouse)
        elif action == 4:
            self.pickup_box(warehouse)
        elif action == 5:
            self.deliver_box(warehouse)

    def move_forward(self, warehouse):
        upd_x = self.x
        upd_y = self.y
        if self.rotation=='N': upd_y+=1
        elif self.rotation=='S':upd_y-=1
        elif self.rotation=='E':upd_x+=1
        elif self.rotation=='W':upd_x-=1
        
        if self.valid_move(warehouse, upd_x, upd_y):
            self.x,self.y= upd_x,upd_y
            self.move_cost+=1
            return True
        return False

    def move_backward(self,warehouse):
        upd_x = self.x
        upd_y = self.y
        if self.rotation=='N': upd_y-=1
        elif self.rotation=='S': upd_y+=1
        elif self.rotation=='E': upd_x-=1
        elif self.rotation=='W': upd_x+=1
        
        if self.valid_move(warehouse, upd_x, upd_y):
            self.x,self.y= upd_x,upd_y
            self.move_cost+=1
            return True
        return False
    
    def rotate_right(self,warehouse):
       rotations = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}
       self.rotation=rotations[self.rotation]
       self.move_cost+=0.5

    def rotate_left(self,warehouse):
       rotations = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
       self.rotation=rotations[self.rotation]
       self.move_cost+=0.5

    
    def pickup_box(self,warehouse):
        if self.c:
            return False
        
        front_x, front_y = self.x, self.y
        if self.rotation == 'N':
            front_y += 1
        elif self.rotation == 'S':
            front_y -= 1
        elif self.rotation == 'E':
            front_x += 1
        elif self.rotation == 'W':
            front_x -= 1

        target_cell=warehouse.grid[front_x][front_y]
        if target_cell.box:
            self.c=target_cell.box
            target_cell.box=None
            return True
        return False
    
    def deliver_box(self,warehouse):
        if not self.c: return False
        
        front_x, front_y = self.x, self.y
        if self.rotation == 'N':
            front_y += 1
        elif self.rotation == 'S':
            front_y -= 1
        elif self.rotation == 'E':
            front_x += 1
        elif self.rotation == 'W':
            front_x -= 1

        target_cell=warehouse.grid[front_x][front_y]
        if target_cell.box is None:
            target_cell.box=self.c
            self.c=None
            return True
        return False
    
    def valid_move(self,warehouse,x,y):
        if not (0 <= x <warehouse.grid_size and 0<=y <warehouse.grid_size):
            return False
        
        if warehouse.grid[x][y].box:
            return False
        
        return True

    


