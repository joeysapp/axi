""""
    Shape onjects are created and referenced in Sketch objects.
    Shape objects are translated into Node objects by the Generator.

    id
    type
    vectors
    params

"""

from .shapes import line, square
from .enums import ShapeType

class Shape(list):
    def __init__(self, id, type, **kwargs):
        Console.init("Shape(id={} type={}{})\n".format(id, type, kwargs))
        self.id = id
        self.type = type
        self.vectors = kwargs.get("vectors") or []
        self.params = kwargs.get("params") or None

        # idk if this werk
        if Shapes.type:
            Shapes.type()

    def __repr__(self):
        vector_string = Console.list(self.vectors)
        return "Shape(id={} type={} params={} vectors={})".format(self.id, self.type, self.params, self.vectors)
