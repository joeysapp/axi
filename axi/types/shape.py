""""
    Shape onjects are created and referenced in Sketch objects.
    Shape objects are translated into Node objects by the Generator.

    id
    type
    vectors
    params

"""

from .enums import ShapeType

from axi.util import Console

class Shape(list):
    def __init__(self, id, type: ShapeType, **kwargs):
        Console.init("Shape(id={} type={}{})\n".format(id, type, kwargs))
        self.id = id
        self.type = type
        self.vectors = kwargs.get("vectors") or []
        self.params = kwargs.get("params") or None
        self.line_length = 0

        # type of ShapeType is used here to call
        # .enums/ShapeType, which points to shapes/
        if type:
            print("type/shape.py, about to call type(params) with params={}".format(self.params))
            self.vectors = type(params=self.params)

    def __repr__(self):
        vector_string = Console.list(self.vectors)
        return "Shape(id={} type={} params={} vectors={})".format(self.id, self.type, self.params, self.vectors)
