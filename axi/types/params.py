"""
   Params objects are used to pass unique information from Generator to Sketch to Shape
"""
from axi.util import Console

class Params():
    def __init__(self, **kwargs):
        Console.init("Params({})\n".format(kwargs))
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    def __repr__(self) -> str:
        return "Params({})".format(self.__dict__)    
