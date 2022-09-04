from axi.util import Console
from axi.math import Vector

# contains an id, neighbors, position
class Node:
    def __init__(self, id=0, pos=None, neighbors=[], text=None):
        self.id = id
        self.pos = pos
        self.neighbors = neighbors
        if text:
            s = text.split(",")
            self.id = s[0]
            self.pos = s[1];

    def __str__(self):
        return "node( id: {} p: {} )".format(self.id, self.p)

class Graph:
    def __init__(self, args, **kwargs):
        self.nodes = {}
        self.length = 0;

        # Python List methods
        # append, e=nd of list
        # extend, iterable to end of list
        # insert(self, index, object)
        # pop(index=-1) remove and return at index
        # remove(self, value) remove first occurrence
        # copy shallow copy of list

    def get(self, idx) -> Action:
        try:
            return self.nodes[idx]
        except:
            return None

    def extend(self, path_extension):
        self.path_entries.extend([ path_extension ])
        self.length += 1

    def load(self, fname):
        with open(fname, "r") as f:
            t = f.read()
            t_list = t.split("\n")
            path_entries = []
            for entry_text in t_list:
                new_entry = PathEntry(text=entry_text)
                path_entries.append(new_entry)
            self.path_entries.extend(path_entries)


    def get_path_as_string(self):
        s = ""
        for path_entry in self.path_entries:
            s += "{},{},{},{},{}\n".format(self.id, self.state, self.pos.x, self.pos.y, self.pos.z);
        return s
    
    def save(self):
        fname = "{}-{}.txt".format(round(time.clock_gettime(0)), len(self.path_entries))
        with open(fname, "w") as f:
            f.write(self.get_path_as_string())
            f.close()
