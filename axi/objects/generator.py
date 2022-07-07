from axi.util import Console
from axi.util import map
from .path import PathEntry
from axi.math import Vector

import random, math

class Generator:
    def __init__(self, args=None, settings={}, **kwargs):
        print("Generator.__init__")
        for k, v in kwargs.items():
            print("Generator.__init__: %s == %s" % (k, v))    
        self.settings = settings

    
    def next(self, path_entry) -> PathEntry:
        # self._generator....
        print('objects/generator/next')
        n = map(random.random(), 0, 1, 0, math.pi * 2)
        path_entry.acc = Vector(math.cos(n), math.sin(n), 0.0)
        path_entry.acc.limit(0.5);

        path_entry.vel.add(path_entry.acc)
        path_entry.vel.limit(1)

        path_entry.pos.add(path_entry.vel)
        x = path_entry.pos.x;
        y = path_entry.pos.y;
        z = path_entry.pos.z;
        [nx, ny, nz] = [x, y, z]

        time = path_entry.time + 1
        pen_pos = path_entry.pen_pos
        if (pen_pos == 1):
            pen_pos = 0

        next_path_entry = PathEntry(pos=Vector(x=nx, y=ny, z=nz), time=time, pen_pos=pen_pos)
        return next_path_entry;
