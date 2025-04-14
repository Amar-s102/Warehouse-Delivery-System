from Warehouse import *
import heapq

class Robot:
    def __init__(self, x,y):
        self.x=x
        self.y=y
        self.rotation= 'R'
        self.lift_height=0
        self.c=0
        self.move_cost=0

    def find_path(self,warehouse,target_x,target_y):
        def heuristic(x1, y1, x2, y2):
            return abs(x1 - x2) + abs(y1 - y2)
        open_set=[]


    def move_forward(self, warehouse):
        if self.rotation=='N': self.y+1
        elif self.rotation=='S':self.y-1
        elif self.rotation=='E':self.x+1
        elif self.rotation=='W':self.x-1
        
        if self.valid_move(warehouse, upd_x, upd_y):
            self.x,self.y= upd_x,upd_y
            self.move_cost+=1
            return True
        return False

    def move_backward(self,warehouse):
        if self.rotation=='N': self.y-1
        elif self.rotation=='S': self.y+1
        elif self.rotation=='E': self.x-1
        elif self.rotation=='W': self.x+1
        
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

    def raise_lift(self):
        if self.lift_height<5:
            self.lift_height+=1
            return True
        return False
    
    def lower_lift(self):
        if self.lift_height>0:
            self.lift_height-=1
            return True
        return False
    
    def pickup_box(self,warehouse):
        if self.c:
            return False
        
        target_cell=warehouse.grid[self.x][self.y]
        if target_cell.shelf and target_cell.shelf.boxes:
            self.c=target_cell.shelf.boxes.pop()
            return True
        return False
    
    def deliver_box(self,warehouse):
        if not self.c: return False
        
        if (self.x , self.y) in warehouse.delivery_points:
            warehouse.delivered_boxes.apped(self.c)
            self.c=None
            return True
        return False
    
    def valid_move(self,warehouse,x,y):
        if not (0 <= x <warehouse.grid_size and 0<=y <warehouse.grid_size):
            return False
        
        if warehouse.grid[x][y].shelf:
            return False
        
        return True

    


