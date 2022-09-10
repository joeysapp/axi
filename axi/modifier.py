import random, math, time
# import opensimplex as osn

from axi.util import Console, fmap, Timer
from axi.types import Vector, Node, Sketch
 
class Modifier():
    def __init__(self, **kwargs):
        Console.init("modifier = Modifier({})\n".format(kwargs))



# modifier / selector, or should it be in the generator... or ... idk



#    # Returns a brand new Shape with new id and new vertices
#    @classmethod
#    def transform(cls, shape, type, x=0, y=0, z=0, degrees=0):
#        new_shape_id = "{}-t={}-x={}-y={}-z={}-d={}".format(shape.id, type, x, y, z, degrees)
#        Console.cls("Shape.transform({} {} x={} y={} z={} degrees={})\n".format(shape.id, type, x, y, z, degrees))
#        new_vertices = []
#        for v in shape.vertices:
#            # lol, shapes not returning Vectors
#            # Console.cls("Shape.vertices[...] : {}\n".format(v))
#            if isinstance(v, list):
#                vx = v[0]
#                vy = v[1]
#                vz = 0 if len(v) < 3 else 0
#            else:
#                vx = v.x
#                vy = v.y
#                vz = v.z
#            # Console.error("vx, vy, vz: {} {} {} \n".format(vx, vy, vz))
#            new_vertex = Vector(x=vx, y=vy, z=vz)
#            if type == 'offset':
#                new_vertex = Vector(x=(vx+x), y=(vy+y), z=(vz+z))
#            elif type == 'scale':
#                new_vertex = Vector(x=(vx*x), y=(vy*y), z=(vz*z))
#           # elif type == 'rotate':
#           #     new_vertex = Vertex()
#           # elif type == 'warp':
#           #     new_vertex = Vertex()
#           # elif type == 'skew':
#           #     new_vertex = Vertex()        
#            new_vertices.append(new_vertex)
#        return cls(id=new_shape_id, type=shape.type, vertices=new_vertices)
