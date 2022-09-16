""""
    Shape objects are created and referenced in Sketch objects.
    Shape objects are translated into Node objects by the Generator.

    id
    type
    params
    vectors

    Vectors are created from ./shapes which pass in a lists of [x y ...z]
"""
from enum import Enum, auto

from .vector import Vector
from .vec3d import v
from .id import TypeId

from axi.util import Console

# from .shapes import line
# from .shapes import rect
# class ShapeType(Enum):
#     line = auto()
#     rect = auto()
#     # rect = rect
#     def __call__(self, params, *args, **kwargs):
#         return eval(self.name)(params, args, kwargs)
#     @classmethod
#     def __str__(cls):
#         return "ShapeType has the following generators and types:\n{}".format(cls.__dict__)
# 
#     def __str__(self):
#         return Console.format("{}".format(self.name), ["cyan"])
# 

class Shape():
    """ Help for the class Shape (axi/types/shape.py)
        An umbrella class capable of generating ShapeTypes and providing helper functions
    """

    @classmethod
    def get_area(cls, vectors):
        return 0

    @classmethod
    def get_line_length(cls, vectors):
        return 0

    @classmethod
    def get_center(cls, vectors):
        return v(0, 0, 0)

    @classmethod
    def get_bounding_box(cls, vectors):
        """
        Shape class method to return a bounding box, a Rect, of supplied list of vectors
        """
        max_x = -(2 ** 32)
        max_y = -(2 ** 32)
        min_x = 2 ** 32
        min_y = 2 ** 32
        for v in vectors:
            if v.x > max_x:
                max_x = v.x
            if v.x < min_x:
                min_x = v.x
            if v.y > max_y:
                max_y = v.y
            if v.y < min_y:
                min_y = v.y
        return [v(min_x, min_y),
                v(max_x, max_y)]

#    @classmethod
#    def contain(self, s1, s2) -> bool:
#        """
#        Shape class method to determine if the first shape completely encompasses the second (and optionally, more) supplised shapes.
#        """
#        within_x = self.min_x < _v.x and _v.x < self.max_x
#        within_y = self.min_y < _v.y and _v.y < self.max_y
#        return within_x and within_y

    def __init__(self, shape_type, params, *args,  **kwargs):
        """ Shape instance method to initialize and populate itself """
        # Console.init("shape.__init__({}, {})\n".format(shape_type, params))
        self.id = TypeId.shape()
        self.type = shape_type
        self.params = params

        self.vectors = AffineTransformation(shape_type(), params)

        self.area = self.get_area(self.vectors)
        self.center = self.get_center(self.vectors)
        self.line_length = self.get_line_length(self.vectors)
        self.bounding_box = self.get_bounding_box(self.vectors)
                
    def __repr__(self):
        vector_string = Console.list(self.vectors)
        return "{}({} type={}, params={}, vectors={})".format(
            Console.format("shape", ["bold"]),
            self.id,
            self.type,
            self.params,
            self.vectors)
        
#
#        return "{}(\n\tid={}\n\ttype={}\n\tparams={}\n\tvectors={}\n)".format(
#            Console.format("Shape", ["cyan", "bold"]),
#            self.id,
#            self.type,
#            self.params,
#            self.vectors)
#


