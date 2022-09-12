"""
   Params objects are used to pass unique information from Generator to Sketch to Shape
"""
from axi.util import Console

# Need a special
# class ParamType(Enum):
    

class Params():
    def __init__(self, **kwargs):
        s = ""
        string = ""
        for k in kwargs:
            s += "{}: {},\t".format(k, kwargs[k])
        Console.init("params.__init__(kwargs={})\n".format(s))
        idx = 0
        for key in kwargs:            
            self.__setattr__(key, kwargs[key])
            string += "{}={}".format(key, str(kwargs[key]))
            if idx < len(kwargs.keys())-1: string += ", "
            idx += 1
        self.string = string

    def __repr__(self) -> str:
        return "{ "+self.string+" }"

    def get(self, str):
        return getattr(self, str)
