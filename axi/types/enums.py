from enum import Enum, auto

class Shapes(Enum):
    line = auto()
    square = auto()

    # Usable like:
    #        vectors = Shapes["line"]()
    def __call__(self, *args, **kwargs):
        return eval(self.name)(args[0] if args else None)


class NodeState(Enum):
    up = auto()
    raise = auto()
    lower = auto()
    down = auto()
    move = auto()

    # Handle all of the state transitions here?
    def __call__(self, **kwargs):
        return eval(self.name)(kwargs)

    # do we want 
    # state = head.state # a NodeState
    # next_state = current_state.get_next(uh, states/position?)

    # cause if all Nodes have a NodeState... these could just be classmethods?


#    @property
#    def primary_colors(self):
#        return self.red, self.blue, self.yellow
#
#    @property
#    def is_primary(self):
#        return self in self.primary_colors
#
#    if some_Color_member.is_primary:
#        do_something()
