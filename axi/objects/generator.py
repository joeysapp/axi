from axi.util import Console
from axi.util import map
from .path import PathEntry
from axi.math import Vector

import random, math

import opensimplex as osn

class Generator:
    def __init__(self, args=None, settings={}, **kwargs):
        print("Generator.__init__")
        for k, v in kwargs.items():
            print("Generator.__init__: %s == %s" % (k, v))    
        self.settings = settings
        osn.seed(42)

    
    def next(self, path_entry) -> PathEntry:
        # self._generator....
        print('objects/generator/next')
        ## creative part 
        x = path_entry.pos.x;
        y = path_entry.pos.y;
        z = path_entry.pos.z;
        ndiv = 16.
        t = path_entry.time / 1000000.;
        n = osn.noise3(x/ndiv, y/ndiv, 0)
        print('\t 001 n =', n, end='\n')
        n = map(n, -1, 1, 0, math.pi * 2)

        path_entry.vel.mult(0.95)

        path_entry.acc = Vector(math.cos(n), math.sin(n), 0.0)
        path_entry.acc.limit(1);
        path_entry.vel.limit(1)

        ## end creative part
        next_vel = path_entry.vel.add(path_entry.acc)
        next_pos = path_entry.pos.add(path_entry.vel)

        if (next_pos.x > 66 or next_pos.x < 33):
            next_pos.x = 33 + random.random()*33.
            next_pos.y = random.random()*225

            next_vel = Vector(0, 0, 0)
        if (next_pos.y > 225 or next_pos.y < 0):
            next_pos.x = 33 + random.random()*33.0
            next_pos.y = random.random()*225
            next_vel = Vector(0, 0, 0)

        time = path_entry.time + 1
        # pen_pos = path_entry.pen_pos
        next_path_entry = PathEntry(pos=next_pos, vel=next_vel, acc=Vector(0, 0, 0), time=time)
        return next_path_entry;
