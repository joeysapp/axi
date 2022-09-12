""""
    Shape onjects are created and referenced in Sketch objects.
    Shape objects are translated into Node objects by the Generator.

    id
    type
    params
    vectors

    Vectors are created from ./shapes which pass in a lists of [x y ...z]

"""
from enum import Enum, auto

from .vector import Vector
from .id import TypeId
#from .shapes.line import line
from .shapes import line

from axi.util import Console


class ShapeType(Enum):
    line = auto()
    square = auto()
    def __call__(self, params, *args, **kwargs):
        return eval(self.name)(params, args, kwargs)
    @classmethod
    def __str__(cls):
        return "ShapeType has the following generators and types:\n"
    # str for enums, interesting
    def __str__(self):
        return Console.format("{}".format(self.name), ["cyan"])




class Shape(list):
    def __init__(self, shape_type, params, *args,  **kwargs):
        Console.init("shape.__init__({}, {})\n".format(shape_type, params))
        self.id = TypeId.shape()
        self.type = shape_type
        self.params = params or None

        self.vectors = kwargs.get("vectors") or []

        self.area = 0
        self.line_length = 0    

        if shape_type:
            xy_list = shape_type(self.params, args, kwargs)
            for xy in xy_list:
                x = xy[0]
                y = xy[1]
                z = 0
                self.vectors.append(Vector(x, y, z))
                
    def __repr__(self):
        vector_string = Console.list(self.vectors)
        return "{}(\n\tid={}\n\ttype={}\n\tparams={}\n\tvectors={}\n)".format(
            Console.format("Shape", ["cyan", "bold"]),
            self.id,
            self.type,
            self.params,
            self.vectors)
