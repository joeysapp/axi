from axi.math import Vector
# from axi.objects import Path

class Square:
    def __init__(self, edge_length, **kwargs):
        for k, v in kwargs.items():
            print("actions/Square __init__: %s == %s" % (k, v))
        self._path = Path()
        self._edge_length = edge_length;
        self.lim = 50;
        self.gen()
    
    @property
    def path(self):
        return self._path

    @property
    def edge_length(self):
        return self._edge_length;
    @edge_length.setter
    def edge_length(self, value):
        try:
            d = float(value)
            if (d < 50):
                self._edge_length = d
        except ValueException as e:
            raise ValueError('square.setattr %s with lim=[%s]' % (value, lim))
            

    def gen(self):
        self._path.push(0, 0)
        self._path.push(0, self._edge_length)
        self._path.push(self._edge_length, self._edge_length)
        self._path.push(self._edge_length, 0)
        self._path.push(0, 0)

