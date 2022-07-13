class Vector:
    def __init__(self, x, y, z, **kwargs):
        self.x = x;
        self.y = y;
        self.z = z;

    def __eq__(self, vector):
        if isinstance(vector, Vector):
            return self.x == vector.x and \
                   self.y == vector.y and \
                   self.z == vector.z
        return False
    
    def __str__(self):
        return '(%f %f %f)' % (self.x, self.y, self.z)

    def __len__(self):
        return self.mag()

    def dist(self, vec) -> float:
        return ((self.x - vec.x) ** 2 + (self.y - vec.y) ** 2) ** 0.5

    def mult(self, f):
        self.x *= f
        self.y *= f
        self.z *= f

    def mag(self):
        return (self.x**2 + self.z**2 + self.z**2)**0.5

    def add(self, vec):
        # self.x += vec.x
        # self.y += vec.y
        # self.z += vec.z
        return Vector(self.x + vec.x, self.y + vec.y, self.z + vec.z);
    
    def limit(self, l):
        if (self.x >= l):
            self.x = l
        elif (self.x <= -l):
            self.x = -l
        if (self.y >= l):
            self.y = l
        elif (self.y <= -l):
            self.y = -l


    # def __lt, le, gt, ge, eq__ (eq and lt needed, and _is_valid_operand)
    # usage: settar(Vector, 'x', value)
    # https://docs.python.org/3/library/functions.html?highlight=setattr#setattr
 
