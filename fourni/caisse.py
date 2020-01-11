class Caisse:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __eq__(self, other):
        if (self.x == other.x) and (self.y == other.y):
            return True
        return False