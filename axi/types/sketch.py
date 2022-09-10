"""
   Sketch objects are referenced in the Generator.
   Sketch objects are used to compose Shape objects.
   Sketch objects are immutable.

   - id
   - shapes
   - bounds
   - total_line_length

"""
from .shape import Shape
from .bounds import Bounds
from axi.util import Console

class Sketch():
    def __init__(self, id, *args, **kwargs):
       Console.init("{} = Sketch(id={}{})\n".format(id, id, "" if not kwargs else kwargs))
       self.id = id
       self.shapes = []
       self.total_line_length = 0

       self.bounds = kwargs.get("bounds") or Bounds()
       if (kwargs.get("sketches")):
           for s in kwargs.get("sketches"):
               self.shapes.extend(s.shapes)
               self.total_line_length += s.total_line_length

    def __repr__(self):
        shapes_string = Console.list(self.shapes)
        return "Sketch(id={} shapes={})".format(self.id, shapes_string)



    def add_shape(self, type, **kwargs):
        Console.method("{}.add_shape(type={}{})\n".format(self.id, type, kwargs if kwargs else ""))

        new_shape_id = self.get_next_shape_id(type)
        new_shape = Shape(id=new_shape_id, type=type, params=kwargs.get("params"))

        self.total_line_length += new_shape.line_length
        self.shapes.append(new_shape)




    def get_next_shape_id(self, type):
        return "{}-{}-{}".format(self.id, self.get_shape_count(), type) 

    def get_shape_count(self):
        return len(self.shapes)






