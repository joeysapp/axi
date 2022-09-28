from axi.types import v
from .__base__ import Shape

def _line():
    return [v(0, 0, 0),
            v(0, 10, 0)]

class line(Shape):
    def __init__(self, **kwargs):
        self.type = "line"
        self.vectors = _line()



        # Global Shape handles of Params
        super(self.__class__, self).__init__(**kwargs)


        # Line-specific Params
        subdivide = kwargs.get("subdivide")
        if (subdivide):
            # this is iterative subdiv
            # 0   [0         1]
            # 1   [0    .5   1]
            # 2   [0 .33 .66 1]
            for idx in range(1, subdivide+1):
                # Look at current x - not 0 and 0, super translated/transformed already.
                x = 0.
                y = 0. + (idx * (1 / (subdivide+1)))
                ins = idx
                self.vectors.insert(ins, v(x, y, 0))

            # what about recursive subdivision:
            # kid named finger:
