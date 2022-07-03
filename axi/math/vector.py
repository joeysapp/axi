class Vector:
    def __init__(self, **kwargs):
        self.pos = [0, 0]
        self.vel = [0, 0]
        self.acc = [0, 0]

        self._x = 0;
        self._y = 0;
        self.xlim = 50;
        self.ylim = 50;
    
    @property
    def x(self):
        return self._x

    # usage: settar(Vector, 'x', value)
    # https://docs.python.org/3/library/functions.html?highlight=setattr#setattr
    @x.setter
    def x(self, value):
        try:
            d = float(value)
            if (d >= 0 and d < self.xlim):
                self._x = d
        except Exception as e:
            raise ValueError('x.setattr %s with lim=[%s %s]' % (value, 0, xlim))

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        try:
            d = float(value)
            if (d >= 0 and d < self.ylim):
                self._y = d
        except Eyception as e:
            raise ValueError('y.setattr %s with lim=[%s %s]' % (value, 0, ylim))

