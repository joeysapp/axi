from axi.util import Console
#from axi.objects import Generator

class PathEntry:
    def __init__(self, pos, vel, acc, pen_position, time):
        self.pos = pos;
        self.vel = vel;
        self.acc = acc;
        self.pen_pos = pen_pos;
        self.time = time;

class Path:
    def __init__(self, args, **kwargs):
        print("Path.__init__")
        for k, v in kwargs.items():
            print("Path.__init__: %s == %s" % (k, v))
        
        self.entries = [ ];
        self.length = 0;
        # append, end of list
        # extend, iterable to end of list
        # insert(self, index, object)
        # pop(index=-1) remove and return at index
        # remove(self, value) remove first occurrence
        # copy shallow copy of list

    def extend(self, path_extension):
        self.entries.extend(path_extension)
    
    def iterative_gen(self):
        # self._generator....
        print('objects/path/iterative_gen')
        path_entry = self._path[self._idx]
        x = path_entry.x
        y = path_entry.y
        z = path_entry.z
        pen_pos = path_entry.pen_pos;
        t = path_entry.t
        t = time.process_time()
        next_entry = PathEntry(x=nx, y=ny, z=nz, t=t, pen_pos=pen_pos)
        self._path.append(next_entry)
