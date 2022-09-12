"""
   Params objects are used to pass unique information from Generator to Sketch to Shape
"""
from axi.util import Console

# Need a special
# class ParamType(Enum):
    

class Params():
    def __init__(self, **kwargs):
        s = ""
        for k in kwargs:
            s += "{}: {},\t".format(k, kwargs[k])
        Console.init("params.__init__(kwargs={})\n".format(s))
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    def __repr__(self) -> str:
        s = ""
        for k in self.__dict__:
            s += "{}: {},".format(k, self.__dict__[k])
        return "params({})".format(s)

    def get(self, str):
        return getattr(self, str)

    def get_all(self):
        param_string = ""
        for k in self.__dict__:
            param_string += "{}: {},".format(k, self.__dict__.get(k))
        return param_string
