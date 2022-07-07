from axi.util import Console
from .path import PathEntry
from axi.math import Vector

class Generator:
    def __init__(self, args=None, settings={}, **kwargs):
        print("Generator.__init__")
        for k, v in kwargs.items():
            print("Generator.__init__: %s == %s" % (k, v))    
        self.settings = settings

    
    def next(self, path_entry) -> PathEntry:
        # self._generator....
        print('objects/generator/next')
        x = path_entry.pos.x;
        y = path_entry.pos.y;
        z = path_entry.pos.z;
        [nx, ny, nz] = [x+1, y+1, z+1]

        time = path_entry.time + 1
        pen_pos = path_entry.pen_pos

        next_path_entry = PathEntry(pos=Vector(x=nx, y=ny, z=nz), time=time, pen_pos=pen_pos)
        return next_path_entry;
