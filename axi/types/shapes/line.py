from axi.types import v
from .__base__ import Shape

from axi.util import Console

def _line():
    return [v(0, 0, 0),
            v(0, 1, 0)]

class line(Shape):
    def __init__(self, **kwargs):
        Console.init("shape.line.__init__(kwargs={})\n".format(kwargs))
        self.type = "line"

        # Create our vectors
        self.vectors = _line()

        # Global Shape ingests Params and applies them to our vectors
        super(self.__class__, self).__init__(**kwargs)



#        subdivide = kwargs.get("subdivide")
#        if (subdivide):
#            # what about recursive subdivision:
#            # this is iterative subdiv
#            # 0   [0         1]
#            # 1   [0    .5   1]
#            # 2   [0 .33 .66 1]
#            for idx in range(1, subdivide+1):
#                # Look at current x - not 0 and 0, super translated/transformed already.
#                x = 0.
#                y = 0. + (idx * (1 / (subdivide+1)))
#                ins = idx
#                self.vectors.insert(ins, v(x, y, 0))
#            # kid named finger:
