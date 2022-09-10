"""
   Params objects are used to pass unique information from Generator to Sketch to Shape
"""
class Params():
    def __init__(self, **kwargs):
        Console.init("Params({})\n".format(kwargs))
        for key in kwargs:
            self.__setattr__(key, kwargs[key])
