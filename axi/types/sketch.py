"""
   Sketch objects are referenced in the Generator.
   Sketch objects are used to compose Shape objects.
   Sketch objects are immutable.

   - id
   - shapes
   - bounds
   - line_length

"""
from .id import TypeId

from axi.util import Console

class Sketch():
    def __init__(self, name, *args, **kwargs):
        s = ""
        for k in kwargs:
            s += "{}: {},\t".format(k, kwargs[k])
        Console.init("sketch.__init__(\"{}\"{})\n".format(name, "\tkwargs={}".format(s)))

        self.id = TypeId.sketch(name)
        self.shapes = []
        self.line_length = 0
        self.bounds = None

        if (kwargs.get("sketches")):
            for other_sketch in kwargs.get("sketches"):
                self.append_sketch(other_sketch)


    def __repr__(self):
        shapes_string = Console.list(self.shapes)
        return "Sketch({} shapes={})".format(self.id, shapes_string)

    def add_shape(self, shape, params):
        Console.method("sketch.add_shape(id={}, type={}, params={})\n".format(self.id, type, params))
        self.shapes.append(shape)
        self.bounds.extend(shape.bounds)
        self.line_length += shape.line_length

    def get_shape_count(self):
        return len(self.shapes)

    def append_sketch(self, other_sketch, **kwargs):
        Console.method("sketch.append_sketch(id={}, {}, {})\n".format(self.id, other_sketch, kwargs if kwargs else ""))
        self.shapes.extend(other_sketch.shapes)
        self.line_length += other_sketch.line_length
