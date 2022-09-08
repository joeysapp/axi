import random, math, time
import opensimplex as osn

from axi.util import Console, fmap, Timer
from axi.math import Vector

from .node import Node

from .shapes.line import line
# from .shapes.square import square


shape_types = [
    "line": eval("line"),
#     "square": eval("square"),
]


""""
    A Shape object is a single primitive shape (that is _not_ closed)
    - id,
    - type,
    - vertices,
    - params,
"""
class Shape():
    # Returns a brand new Shape with new id and new vertices
    @classmethod
    def transform(cls, shape, type, x=0, y=0, z=0, degrees=0):
        Console.method("Shape.transform({} {} {} {} {} {})\n".format(shape.id, type, x, y, z, degree))
        new_vertices = []
        for v in self.vertices:
            new_vertex = Vertex(v.x, v.y, v.z)
            if type == 'offset':
                new_vertex = Vertex(v.x+x, v.y+y, v.z+z)
            elif type == 'scale':
                new_vertex = Vertex(v.x*x, v.y*y, v.z*z)
           # elif type == 'rotate':
           #     new_vertex = Vertex()
           # elif type == 'warp':
           #     new_vertex = Vertex()
           # elif type == 'skew':
           #     new_vertex = Vertex()        
            new_vertices.append(new_vertices)
        new_shape_id = "{}-{}-{}-{}-{}-{}".format(shape.id, type, x, y, z, degrees)
        return cls(id=new_shape_id, vertices=new_vertices)


    def __init__(self, id, type, vertices=[], params={}):
       Console.init("Shape(id={}, type={}, vertices={}, params={})\n".format(id, type, vertices, params));
       self.id = id
       self.type = type
       self.vertices = vertices
       self.params = params

    def gen(self):
        Console.method("Shape.gen(id={} type={} vertices={} params={})\n".format(self.id, self.type, self.vertices, self.params))
        self.vertices = shape_types[self.type](self.params)



"""

   A Plot object contains a list of Shapes (a Shape is itself a list of vertices)
   They themselves can be used to create other Plots.
   - id,
   - shapes = [], // ordered list

"""
class Plot():
    # Returns a brand new Plot with new id and new shapes
    @classmethod
    def transform(cls, plot, type, x=0, y=0, z=0, degrees=0):
        Console.method("Plot.transform({} {} {} {} {})\n".format(plot.id, type, x, y, z, degree))
        new_shapes = []
        for shape in plot.shapes:
            new_shape = Shape.transform(shape, x, y, z, degrees)
            #new_shape = Shape.offset(shape, x, y)
            new_shapes.append(new_shape)
        new_id = "{}-{}-{}-{}-{}-{}".format(plot.id, transform_type, x, y, z, degrees)
        return cls(id=new_id, shapes=new_shapes)


    def __init__(self, id, shapes=[]):
       Console.init("Plot(id={} shapes={})\n".format(id, shapes)
       self.id = id
       self.shapes = shapes

    def __repr__(self):
        return "Plot(id={} shapes={})".format(self.id, self.shapes)

    def add_shape(self, type, params={}):
        Console.method("Plot.add_shape(type={} params={})\n".format(type, params))

        new_shape_id = "{}-{}-{}".format(self.id, self.get_shape_count(), type)
        new_shape = Shape(id={new_shape_id}, type=type, params=params)

        self.shapes.append(new_shape)

    def gen(self):
        Console.method("Plot.gen()\n"
        for shape in self.shapes:
            shape.gen()

    def get_shape_count(self):
        return len(self.shapes)
           




class Generator():
    def __init__(self, plots={}):
        Console.init("Generator(plots={})\n".format(plots))

        # Generator itself does not care about which Plot was first,
        # We keep track of that in Scheduler. We store Plots here
        # for any future modification/plotting of NEW Plots.
        self.plots = {}

    def __repr__(self):
        return "Generator({})".format(self.__dict__)

    def create_plot(self, id):
        if id in self.plots:
            Console.error("Generator.create_plot(id={}) -> {} in self.plots\n".format(id, id))
        elif (id and type):
            Console.method("Generator.create_plot(id={})\n".format(id))
            self.plots[id] = Plot(id);

    def get_plot_nodes(self, id):
        if not (id in self.plots):
            Console.error("Generator.get_plot_nodes(id={)) -> {} not in self.plots\n".format(id))
        else:
            Console.method("Generator.get_plot_nodes(id={))\n".format(id))
            shapes = self.plts[id].shapes
            nodes = Translate.get_shapes_as_nodes(shapes)
            return nodes


"""
   Translates a plot's Shapes into Nodes
      * Node.pos is unchanged
      * Node.id is unchanged
      * Node.state is set (up/down/raise/lower/move/ ... wait/start/end)

    Removes the overhead of generating Node state elsewhere, and allows for //DYNAMIC CONTENT//
"""
class Translator():
    @classmethod()
    def get_shapes_as_nodes(cls, id, shapes):
        Console.class("Translator.get_shapes_as_nodes(id={} shapes={})".format(id, shapes))
        nodes = {}
        idx = 0
        for shape in shapes:
            
            # nodes[Node] = Node()
            idx += 1
        return nodes
