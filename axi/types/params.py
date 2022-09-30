"""
Params objects are used to pass unique information from Generator to Sketch to Shape.
They are essentially a wrapper around what would be **kwargs
"""

from axi.types import v
from axi.util import Console

class Params(dict):
    def __init__(self, **kwargs):
        Console.init("params.__init__(kwargs={})\n".format(kwargs))
        # We first transform a shape's generated vectors, then translate them.
        # https://en.wikipedia.org/wiki/Transformation_matrix
        self.transformation = None

        # A translation is an affine transformation with the origin as a fixed poiont
        # https://en.wikipedia.org/wiki/Translation_(geometry)
        self.translation = None

        pos = kwargs.get("pos")
        if (pos):
            self.translation = [0, 0, 0]            
            # Create our translation matrix
        degrees = kwargs.get("degrees")
        radians = kwargs.get("radians")
        if degrees or radians:
            self.transformation = [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
            # Apply a rotation matrix

        
        length = kwargs.get("length")
        if length:
            self.transformation = [[0, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]]
            # Apply a ... scaling? Homothety? matrix


        for key in kwargs:            
            self.__setattr__(key, kwargs[key])

    def __repr__(self) -> str:
        s = ""
        for key in self.__dict__:
            s += "\t- {}: {}\n".format(key, getattr(self, key))
        return "Params(\n{}\t)".format(s)

    def get(self, str):
        return getattr(self, str)

    def get_transformation_matrix(self):
        return None

    def get_translation_matrix(self):
        return None
