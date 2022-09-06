from axi.util import Console

class Node:
    def __init__(self, *args, **kwargs):
        Console.init("Node.__init__({})\n".format(kwargs))

        self.id = kwargs.get("id") or None
        self.state = kwargs.get("state") or None
        self.pos = kwargs.get("pos") or None
        self.next = kwargs.get("next") or None
        self.prev = kwargs.get("prev") or None
        self.neighbors = kwargs.get("neighbors") or None

        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    def __repr__(self):
        return "Node.__repr__({})".format(self.__dict__)
#        return "{},{},{},{},prev={},next={},neighbors=".format(self.id, self.state, self.pos, self.prev, self.next, self.neighbors)

    def set_id(self, id):
        self.id = id

    def set_state(self, state):
        self.state = state

    def set_pos(self, pos):
        self.pos = pos
        
    def set_next(self, next):
        self.next = next
        
    def set_prev(self, prev):
        self.prev = prev

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors


# ease of making a Node(....................)

#        versus setattr/getattr?

    # def set_pos(self, ...
