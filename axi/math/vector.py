# todo(@joeysapp on 2022-09-03):
# - https://docs.python.org/3/library/functions.html?highlight=setattr#setattr
# - settar(Vector, 'x', value) vs. my_vector.setX(value);

class Vector:
    def __init__(self, x=None, y=None, z=None, list=[]):
        if (len(list) >= 2):
            self.x = list[0]
            self.y = list[1]
            self.z = 0 if len(list) < 3 else list[2]
        else:
            self.x = x
            self.y = y
            self.z = z

    def __eq__(self, vector):
        if isinstance(vector, Vector):
            return self.x == vector.x and \
                   self.y == vector.y and \
                   self.z == vector.z
        return False

    def __repr__(self) -> str:
        return "{},{},{}".format(self.x, self.y, self.z);    
    
    def __str__(self) -> str:
        return "{},{},{}".format(self.x, self.y, self.z);

    def mag(self):
        return (self.x**2 + self.z**2 + self.z**2)**0.5

    def dist(self, vec) -> float:
        # note(@joeysapp): ** faster than math.pow, no fn call
        return ((self.x - vec.x)**2 +
                (self.y - vec.y)**2 +
                (self.z - vec.z)**2)**0.5

    def mult(self, f):
        return Vector(self.x * f, self.y * f, self.z * f)

    @classmethod
    def add(cls, v1, v2):
        return cls(v1.x+v2.x, v1.y+v2.y, v1.z+v2.z)

    @classmethod
    def sub(cls, v1, v2):
        return cls(v1.x-v2.x, v1.y-v2.y, v1.z-v2.z)

#    def add(self, vec):
#        return Vector(self.x + vec.x, self.y + vec.y, self.z + vec.z)
