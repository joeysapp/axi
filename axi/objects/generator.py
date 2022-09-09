import random, math, time
# import opensimplex as osn

from axi.util import Console, fmap, Timer
from axi.math import Vector

from .node import Node

from .shapes.line import line
from .shapes.square import square

shape_types = {
    "line": eval("line"),
    "square": eval("square"),
}


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
        new_shape_id = "{}-t={}-x={}-y={}-z={}-d={}".format(shape.id, type, x, y, z, degrees)
        Console.cls("Shape.transform({} {} x={} y={} z={} degrees={})\n".format(shape.id, type, x, y, z, degrees))
        new_vertices = []
        for v in shape.vertices:
            # lol, shapes not returning Vectors
            # Console.cls("Shape.vertices[...] : {}\n".format(v))
            if isinstance(v, list):
                vx = v[0]
                vy = v[1]
                vz = 0 if len(v) < 3 else 0
            else:
                vx = v.x
                vy = v.y
                vz = v.z
            # Console.error("vx, vy, vz: {} {} {} \n".format(vx, vy, vz))
            new_vertex = Vector(x=vx, y=vy, z=vz)
            if type == 'offset':
                new_vertex = Vector(x=(vx+x), y=(vy+y), z=(vz+z))
            elif type == 'scale':
                new_vertex = Vector(x=(vx*x), y=(vy*y), z=(vz*z))
           # elif type == 'rotate':
           #     new_vertex = Vertex()
           # elif type == 'warp':
           #     new_vertex = Vertex()
           # elif type == 'skew':
           #     new_vertex = Vertex()        
            new_vertices.append(new_vertex)
        return cls(id=new_shape_id, type=shape.type, vertices=new_vertices)


    def __init__(self, id, type, vertices=[], params={}):
       # Console.init("{} = Shape(id={}, type={}, vertices={}, params={})\n".format(id, id, type, vertices, params));
       self.id = id
       self.type = type
       self.vertices = vertices
       self.params = params
       self.vertices = vertices if len(vertices) else shape_types[self.type].get()

    def __repr__(self):
        return "Shape.{}.(id t={} v={} p={})".format(self.id, self.type, self.vertices, self.params)

    def gen(self):
        Console.method("shape.{}.gen(id t={} v={} p={})\n".format(self.id, self.type, self.vertices, self.params))
        return self


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
       Console.init("{} = Plot(id={} shapes={})\n".format(id, id, shapes))
       self.id = id
       self.shapes = shapes

    def __repr__(self):
        return "Plot(id={} shapes={})".format(self.id, self.shapes)

    def add_shape(self, type, params={}):
        Console.method("{}.add_shape(type={} params={})\n".format(self.id, type, params))

        new_shape_id = "{}-{}-{}".format(self.id, self.get_shape_count(), type)
        new_shape = Shape(id=new_shape_id, type=type, params=params)

        #new_shape_1 = Shape.transform(new_shape, type="scale", x=10, y=10)
        #Console.method("plot.add_shape result is -> {}\n".format(new_shape_1))
        #self.shapes.append(new_shape_1)
        self.shapes.append(new_shape)

    def get_shape_count(self):
        return len(self.shapes)



class Generator():
    def __init__(self, plots=[], *args, **kwargs):
        Console.init("generator = Generator({})\n".format(kwargs))

        # Generator itself does not care about which Plot was first,
        # We keep track of that in Scheduler. We store Plots here
        # for any future modification/plotting of NEW Plots.
        self.plots = {}

    def __repr__(self):
        return "Generator({})".format(self.__dict__)
    
    def create_plot(self, id, plots=[]) -> Plot:
        """ Returns a plot for easy Plot creation in main """
        if id in self.plots:
            Console.error("generator.create_plot(id={}) -> {} in self.plots\n".format(id, id))
        if len(plots) > 0:
            Console.method("generator.create_plot(id={} plots={})\n".format(id, plots))
            Console.error("generator.create_plot(id={} plots={}) -> not implemented\n".format(id, plots))
        else:
            Console.method("generator.create_plot(id={})\n".format(id))
            self.plots[id] = Plot(id)
            return self.plots[id]

    def get_nodes_for_scheduler(self, id):
        if not (id in self.plots):
            Console.error("generator.get_nodes_for_scheduler(id={}) -> {} not in self.plots\n".format(id, id))
        else:
            Console.method("generator.get_nodes_for_scheduler(id={})\n".format(id))

            shapes = self.plots[id].shapes
            nodes, head = self.translate_shapes_to_nodes(plot_id=id, shapes=shapes)
            Console.method("generator.get_nodes_for_scheduler(id={})".format(id))
            Console.puts("\n\t-> {}\n".format(
                Console.format("(temporary.nodes {})".format(len(nodes.keys())), ["bold", "green"])))

            return nodes, head

    def translate_shapes_to_nodes(self, plot_id, shapes, scheduler_head=None):
        Console.method("generator.translate_shapes_to_nodes(id={}, shapes=[{} shapes], scheduler_head={})\n"
                       .format(plot_id,
                               len(shapes),
                               "None"))

        # For now, assume all plots return to origin??
        # Otherwise, we need to know where the Scheduler's head is.......
        # ....

        scheduler_head = None
        head_node = None
        next_node = None
        prev_node = None
        nodes = {}

        debug = False


        # lol idk how references work
        # espcially in python

        shape_idx = 0
        for shape in shapes:
            shape_type = shape.type
            vertex_idx = 0
            for vertex in shape.vertices:

                # (plot-id)-(shape-idx)-(shape-type)-(vertex-idx)
                node_id = "{}-{}-{}-{}".format(plot_id, shape_idx, shape_type, vertex_idx)
                node_pos = Vector(0, 0, 0)
                node_state = "up"

                if (head_node == None):
                    # Beginning of Nodes
                    head_node = Node(pos=node_pos, state=node_state, id=node_id)
                    first_node_id = node_id
                else:
                    # head already exists -  so we need to create a new Node,
                    # set that head.next as the new Node we create, then set the head as that new node
                    
                    tmp_next_node = Node(pos=node_pos, state=node_state, id=node_id)
                    if debug: print('\n0', tmp_next_node, "\t", head_node)

                    head_node.next = tmp_next_node.id
                    if debug: print('1', tmp_next_node, "\t", head_node)

                    tmp_next_node.prev = head_node.id
                    if debug: print('2', tmp_next_node, "\t", head_node)

                    head_node = tmp_next_node
                    if debug: print('3', tmp_next_node, "\t", head_node)
                    

                vertex_idx += 1
                if (debug): print("head is now:", head_node)
                # Console.puts("Adding this head node: {}\n".format(head_node))
                nodes[node_id] = head_node
            shape_idx += 1

#        Console.method("generator.translate_shapes_to_nodes(plot_id={}, shapes=[2 shapes], scheduler_head={})\n"
#                       .format(plot_id,
#                               len(shapes),
#                               "None"))
#        Console.puts("="*80+"\n");
        Console.puts("\t-> A linked list of {} was created\n".format(
            Console.format(str(len(nodes.keys()))+" Nodes", ["bold", "green"])))

        Console.puts("\t-> The head of this linked list is: {}\n".format(
            Console.format(first_node_id, ["bold", "green"])))
        for k in nodes.keys():
            Console.puts("\t{}\n".format(nodes[k]))

        return nodes, first_node_id
            # Finishing looping through Shape's vertices.
            # Do we need to raise, or do we leave that for the next iteration?
            


"""
   Translates a plot's Shapes into Nodes
      * Node.pos is unchanged
      * Node.id is unchanged
      * Node.state is set (up/down/raise/lower/move/ ... wait/start/end)

    Removes the overhead of generating Node state elsewhere, and allows for //DYNAMIC CONTENT//

    It needs to do the following with a list of Shapes:
    * Start and end the Plot properly (up/down)
    * Handle shape "closing"
    * Handle shapes being connected - both the Node.next/prev, and if the pen needs to raise.


"""
