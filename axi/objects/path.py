from axi.util import Console
from axi.math import Vector
#from axi.objects import Generator

class PathEntry:
    def __init__(self, pos=Vector(0, 0, 0), vel=Vector(0, 0, 0), acc=Vector(0, 0, 0), pen_pos=1, time=0):
        self.pos = pos;
        self.vel = vel;
        self.acc = acc;
        self.pen_pos = pen_pos;
        self.time = time;

    def __str__(self):
        return 'PathEntry(\n\tpos=%s\n\tvel=%s\n\tacc=%s\n\tpen_pos=%s\n\ttime=%s\n)' % (self.pos, self.vel, self.acc, self.pen_pos, self.time)

class Path:
    def __init__(self, args, initial_path_entry=None, path_entries=None, **kwargs):
        print("Path.__init__")
        for k, v in kwargs.items():
            print("Path.__init__: %s == %s" % (k, v))
        
        if initial_path_entry:
            self.path_entries = [initial_path_entry]
        else:
            self.path_entries = [PathEntry()]
        self.length = 0;
        # append, e=nd of list
        # extend, iterable to end of list
        # insert(self, index, object)
        # pop(index=-1) remove and return at index
        # remove(self, value) remove first occurrence
        # copy shallow copy of list

    def get(self, idx) -> PathEntry:
        return self.path_entries[idx]

    def extend(self, path_extension):
        self.path_entries.extend([ path_extension ])
        self.length += 1
