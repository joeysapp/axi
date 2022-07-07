class Vector:

 #   def mag(vec):
#  return (vec[0]**2 + vec[1]**2)**0.5

    def __init__(self, x, y, z, **kwargs):
        self.x = x;
        self.y = y;
        self.z = z;
    
    def __str__(self):
        return '(%f %f %f)' % (self.x, self.y, self.z)

    def add(self, vec):
        self.x += vec.x
        self.y += vec.y
        self.z += vec.z
    
    def limit(self, l):
        if (self.x > l):
            self.x = l
        elif (self.x < -l):
            self.x = -l
        if (self.y > l):
            self.y = l
        elif (self.y < -l):
            self.y = -l


    # def __lt, le, gt, ge, eq__ (eq and lt needed, and _is_valid_operand)
    # usage: settar(Vector, 'x', value)
    # https://docs.python.org/3/library/functions.html?highlight=setattr#setattr
 
