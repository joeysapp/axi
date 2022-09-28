"""
   Nodes are translated into Shapes by the Generator
   Nodes are made into a doubly linked list by the Generator.
   Nodes are used by the Scheduler to interface with Serial.

   id
   pos
   state

   next
   prev
   neighbors

"""
from enum import Enum, auto

from axi.util import Console
from .id import TypeId

class Node:
    def __init__(self, shape_id, **kwargs):
        # Console.init("Node(shape_id={} {})\n".format(shape_id, kwargs))        
        self.id = TypeId.node(shape_id)

        # note(joeysapp): a [0,0,0] v is considered None? is that an __eq__ thing?
        self.pos = kwargs.get("pos")
        self.state = kwargs.get("state") or None

        self.next = kwargs.get("next") or None
        self.prev = kwargs.get("prev") or None

        self.neighbors = kwargs.get("neighbors") or []
        # Console.init("Node {}\n".format(self.__dict__))

    def set_state(self, state):
        self.state = state        

    def set_next(self, id):
        self.next = id

    def set_pos(self, pos):
        self.pos = pos

    # def set_prev(self, id):
    #     self.prev = id

    def __repr__(self):
        #return "Node(id={} prev={} next={} state={} pos={})".format(self.id[-5:], self.prev[-5:] if self.prev else "None", self.next[-5:] if self.next else "None", self.state, self.pos)
        id_len = 15
        id_style = []
        return "node({}\t{}\t{}\t{}\t{}\t)".format(
            Console.format("{}".format(self.id), id_style),
            Console.format("\tprev=None" if self.prev == None else "\tprev={}".format(self.prev[-id_len:]), "gray-0"),
            Console.format("\tnext=None" if self.next == None else "\tnext={}".format(self.next[-id_len:]), "gray-0"),
            self.pos,
            self.state)


# ... hmmmm... Usable like:
# head_state = NodeState.up
# next_state = head_state.get_next(head_node, tmp_node)

class NodeState(Enum):
    up = auto()
    ascend = auto()
    descend = auto()
    down = auto()
    move = auto()

    def __str__(self):
        style = []
        if self == NodeState.up:
           style.extend(["green", "bold"])
        elif self == NodeState.down:
           style.extend(["red", "bold"])
        elif self == NodeState.move:
           style.extend(["italic", "gray-1"])
        elif self == NodeState.descend:
           style.extend(["yellow", "bold"])
        elif self == NodeState.ascend:
           style.extend(["yellow", "bold"])

        s = Console.format(self.name, style)
        return s
        # return self.name

    def get_next(**kwargs):    
        return NodeState.ascend

    def is_up(self):
        return self.name == 'up'
    
    def is_raising(self):
        return self.name == 'ascend'

    def is_lowering(self):
        return self.name == 'descend'

    def is_down(self):
        return self.name =='down'

    def is_moving(self):
        return self.name == 'move'
