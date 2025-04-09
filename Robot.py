class Robot:
    def __init__(self, x,y):
        self.x=x
        self.y=y
        self.rotation= 'R'
        self.lift_height=0
        self.C=0
        self.move_cost=0

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
