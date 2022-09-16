from axi.types import Shape
from .line import line

def rect():
    return [line([0, 0], [0, 1]),
            line([0, 1], [1, 1]),
            line([1, 1], [1, 0]),
            line([1, 0], [0, 0])]

class Rect(Shape):
    def __init__(self, **kwargs):
        self.type = "rect"
        self.vecs = rect()        

        super(self, **kwargs)
        
        return self.vecs
