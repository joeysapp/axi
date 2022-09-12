
from .id import TypeId

from axi.util import Console

class Vector:
#    @classmethod
#    def norm(cls, v1):
#        m = v1.mag()
#        return cls.div(v1, m)

    @classmethod
    def copy(cls, v1):
        return cls(v1.x, v1.y, v1.z)

    @classmethod
    def add(cls, v1, v2):
        return cls(v1.x+v2.x, v1.y+v2.y, v1.z+v2.z)

    @classmethod
    def sub(cls, v1, v2):
        return cls(v1.x-v2.x, v1.y-v2.y, v1.z-v2.z)

    @classmethod
    def mult(cls, v1, v2):
        if isinstance(v2, Vector):
            return cls(v1.x*v2.x, v1.y*v2.y, v1.z*v2.z)
        else:
            return cls(v1.x*f, v1.y*f, v1.z*f)

    @classmethod
    def div(cls, v1, v2):
        if isinstance(v2, Vector):
            return cls(v1.x/v2.x, v1.y/v2.y, v1.z/v2.z)
        else:
            return cls(v1.x/f, v1.y/f, v1.z/f)


    def __init__(self, x=0, y=0, z=0):
        # self.id = TypeId.vector()
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        left_max = 3

        x = "{:.1f}".format(self.x).split('.')
        x_neg = True if self.x < 0 else False
        x_str = "{}.{}".format(x[0].rjust(left_max, "0"), x[1])

        y = "{:.1f}".format(self.y).split('.')
        y_neg = True if self.y < 0 else False    
        y_str = "{}.{}".format(y[0].rjust(left_max, "0"), y[1])

        z = "{:.1f}".format(self.z).split('.')
        z_neg = True if self.z < 0 else False 
        z_str = "{}.{}".format(z[0].rjust(left_max, "0"), z[1])

        return Console.format("({},\t{})".format(x_str, y_str), [])
        # return Console.format("({}, {})".format(x_str, y_str), ["black", "bg-gray-0"])

    def __eq__(self, v2):
        if isinstance(v2, Vector):
            return self.x == v2.x and \
                   self.y == v2.y and \
                   self.z == v2.z
        return False

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def dist(self, vec) -> float:
        # note(@joeysapp): ** faster than math.pow, no fn call
        return ((self.x - vec.x)**2 +
                (self.y - vec.y)**2 +
                (self.z - vec.z)**2)**0.5
