""""
    Shape objects are created and referenced in Sketch objects.
    Shape objects are translated into Node objects by the Generator.

    id
    type
    params
    vectors

"""
from enum import Enum, auto

from axi.types import v, TypeId, Params

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
    """
    Help for the class Shape (axi/types/shape.py)
    An abstract class that all shapes inherit with general properties and methods
    """

    @classmethod
    def _set_area(cls, vectors):
        return 0

    @classmethod
    def _set_line_length(cls, vectors):
        return 0

    @classmethod
    def _set_center(cls, vectors):
        return v(0, 0, 0)

    @classmethod
    def _set_bounding_box(cls, vectors):
        """
        Shape class method to return a bounding box, a Rect, of supplied list of vectors
        """
        max_x = -(2 ** 32)
        max_y = -(2 ** 32)
        min_x = 2 ** 32
        min_y = 2 ** 32
        for vec in vectors:
            if vec.x > max_x:
                max_x = vec.x
            if vec.x < min_x:
                min_x = vec.x
            if vec.y > max_y:
                max_y = vec.y
            if vec.y < min_y:
                min_y = vec.y
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

    def __init__(self, **kwargs):
        """ Shape instance method to initialize and populate itself """
        self.id = TypeId.shape()
        self.params = Params(**kwargs)

        # could be a way of undoing actions on things, like
        # give me a new square that doesn't have that last transformation..
        self.actions = []

        # self.vectors = AffineTransformation(shape_type(), params)
        self.vectors = self.vectors

        self.area = self._set_area(self.vectors)
        self.center = self._set_center(self.vectors)
        self.line_length = self._set_line_length(self.vectors)
        self.bounding_box = self._set_bounding_box(self.vectors)

                
    def __repr__(self):
        return "Shape(type={}\tid={}\tparams=...\tvectors={}\n".format(
            Console.format(self.type, ["blue", "underline"]),
            self.id,
            # self.params,
            Console.list(self.vectors))
