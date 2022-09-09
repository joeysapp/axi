from axi.util import Console

class Node:
    def __init__(self, *args, **kwargs):
        # Console.init("Node({})\n".format(kwargs))

        self.id = kwargs.get("id") or None
        self.state = kwargs.get("state") or None
        self.pos = kwargs.get("pos") or None
        self.next = kwargs.get("next") or None
        self.prev = kwargs.get("prev") or None
        self.neighbors = kwargs.get("neighbors") or None
        for key in kwargs:
            self.__setattr__(key, kwargs[key])
        Console.init("{}\n".format(self))

    def __repr__(self):
        #return "Node(id={} prev={} next={} state={} pos={})".format(self.id[-5:], self.prev[-5:] if self.prev else "None", self.next[-5:] if self.next else "None", self.state, self.pos)
        id_len = 12
        return "Node(pos={} state={} {} {} {})".format(
            self.pos,
            self.state,
#            Console.format("id=..{}".format(self.id[-id_len:]), [""]),
            "id=..{}".format(self.id[-id_len:]),
            Console.format("None" if self.prev == None else "prev=..{}".format(self.prev[-id_len:]), "gray-0"),
            Console.format("None" if self.next == None else "next=..{}".format(self.next[-id_len:]), "gray-0"))

#            Console.format("prev=..{}".format(self.prev[-id_len:]) if self.prev else "None", "gray-0"),
#            Console.format("next=..{}".format(self.next[-id_len:]) if self.next else "None", "gray-0"))

        # return "Node({})".format(self.__dict__)

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
