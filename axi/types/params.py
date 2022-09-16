"""
Params objects are used to pass unique information from Generator to Sketch to Shape.
They are essentially a wrapper around what would be **kwargs, but I would like them to
act almost like Shapes themselves - imagine the following scenario

Plus, think about:
   p.width = (logic to parse out args)
   p.get_props():
       
base_params = { pos, degrees }
for i in loop():

    # do something complex, like rotate and change a transformation matrix all in one op
    new_params = Params.do_action(base_params, thing)
    s = Line(new_params)

idk. thankabowtit

"""
from axi.util import Console

class Params(dict):
    def __init__(self, **kwargs):
        Console.init("params.__init__(kwargs={})\n".format(s))
        self.width = 1;
        self.height = 1;
        self.length = 1;

        self.v = v(0, 0, 0)
        self.v1 = v(0, 0, 0)
        self.v2 = v(0, 1, 0)
        # self.v3 ...

        # Matrices accomplish actual generation,
        # A translation is an affine transformation with the origin as a fixed poiont
        # https://en.wikipedia.org/wiki/Translation_(geometry)
        self.translation_matrix = None
        # Offsets
        self.o_x = 0
        self.o_y = 0
        self.o_z = 0
        self.o_v = None
        self.o_v1 = None
        self.o_v2 = None    

        # https://en.wikipedia.org/wiki/Transformation_matrix
        self.transformation_matrix = None
        # Stretching        
        # Squeezing
        # Rotation    
        self.degrees = 0
        self.radians = 0
        # Shearing
        # https://en.wikipedia.org/wiki/Shear_matrix
        # Reflection
        # Orthagonal projection

        for key in kwargs:            
            self.__setattr__(key, kwargs[key])
        


    def __repr__(self) -> str:
        return "{ "+self.string+" }"

    def get(self, str):
        return getattr(self, str)





    def get_transformation_matrix(self):
        return None

    def get_translation_matrix(self):
        return None
