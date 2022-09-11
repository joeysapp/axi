from enum import Enum, auto

from .shapes.line import line



# Usable like:
# list_of_xy_list = ShapeType.line(params=Params(...))
class ShapeType(Enum):
    line = auto()
    square = auto()

    def __call__(self, *args, **kwargs):
        return eval(self.name)(args, kwargs)


# Usable like:
# head_state = NodeState.up
# next_state = head_state.get_next(head_node, tmp_node)

class NodeState(Enum):
    up = auto()
    ascend = auto()
    descend = auto()
    down = auto()
    move = auto()

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
