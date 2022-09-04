import random, math, time
import opensimplex as osn

from axi.util import Console, fmap
from axi.math import Vector
from .graph import Graph, Node
# from .shapes import Square


class Generator:
    def __init__(self, args):
        Console.log("Generator.__init__( args={} )\n".format(args))
        osn.seed(42)

    # Returns a dictionary of nodes generated?
    # but how 2 know where 2 start.
    def do(self, cmd, head, bounds):
        Console.log("Generator.do( cmd={}, heads={}, bounds={} )\n".format(cmd, head, bounds))
        nodes = {}

        nodes[0] = Node(id=0, action="move", pos=Vector(50, 50, 0), neighbors=[1])
        nodes[1] = Node(id=1, action="lower", pos=Vector(50, 50, 0), neighbors=[2])
        nodes[2] = Node(id=2, action="move", pos=Vector(50, 100, 0), neighbors=[3])
        nodes[3] = Node(id=3, action="raise", pos=Vector(50, 100, 0), neighbors=[])
        
        return nodes







#    def get_shape_path(self, type, pos, options) -> Path:
#        path = None
#        if (type == 'square'):
#            path = Square(pos, options)
#        elif (type == 'circle'):
#            path = Circle(pos, options)
#        elif (type == 'spiral'):
#            path = Spiral(pos, options)
#    
#    def _next_simplex_fun(self, path_entry) -> PathEntry:
#        # self._generator....
#        print('objects/generator/next')
#        ## creative part 
#        x = path_entry.pos.x;
#        y = path_entry.pos.y;
#        z = path_entry.pos.z;
#        ndiv = 16.
#        t = path_entry.time / 1000000.;
#        n = osn.noise3(x/ndiv, y/ndiv, 0)
#        print('\t 001 n =', n, end='\n')
#        n = map(n, -1, 1, 0, math.pi * 2)
#
#        path_entry.vel.mult(0.95)
#
#        path_entry.acc = Vector(math.cos(n), math.sin(n), 0.0)
#        path_entry.acc.limit(1);
#        path_entry.vel.limit(1)
#
#        ## end creative part
#        next_vel = path_entry.vel.add(path_entry.acc)
#        next_pos = path_entry.pos.add(path_entry.vel)
#
#        if (next_pos.x > 66 or next_pos.x < 33):
#            next_pos.x = 33 + random.random()*33.
#            next_pos.y = random.random()*225
#
#            next_vel = Vector(0, 0, 0)
#        if (next_pos.y > 225 or next_pos.y < 0):
#            next_pos.x = 33 + random.random()*33.0
#            next_pos.y = random.random()*225
#            next_vel = Vector(0, 0, 0)
#
#        time = path_entry.time + 1
#        # pen_pos = path_entry.pen_pos
#        next_path_entry = PathEntry(pos=next_pos, vel=next_vel, acc=Vector(0, 0, 0), time=time)
#        return next_path_entry;
#
