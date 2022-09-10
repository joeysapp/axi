class Vector:
#    @classmethod
#    def norm(cls, v1):
#        m = v1.mag()
#        return cls.div(v1, m)

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
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return "({:.4f} {:.4f} {:.4f}}".format(self.x, self.y, self.z)

    def __eq__(self, v2):
        if isinstance(v2, Vector):
            return self.x == v2.x and
                   self.y == v2.y and
                   self.z == v2.z
        return False

    def mag(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def dist(self, vec) -> float:
        # note(@joeysapp): ** faster than math.pow, no fn call
        return ((self.x - vec.x)**2 +
                (self.y - vec.y)**2 +
                (self.z - vec.z)**2)**0.5

    


#    def add(self, vec):
#        return Vector(self.x + vec.x, self.y + vec.y, self.z + vec.z)
#    def mult(self, f):
#        return Vector(self.x*f, self.y*f, self.z*f)
