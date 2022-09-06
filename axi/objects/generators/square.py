from ..node import Node

from axi.math import Vector

class Square():
    @classmethod
    def get_id(cls, base, id):
        return None if id < 0 else "{}-{}".format(base, id)
    
    @classmethod
    def get(cls, *args, **kwargs):
#        for key in kwargs:
#           self.__setattr__(key, kwargs[key])

        base_id = kwargs.get('id')
        next_id = None
        prev_id = None

        head = "{}-{}".format(base_id, 0)
        nodes = {}

        # not smart
        width = kwargs.get('width')
        height = kwargs.get('height')

        pos = Vector(0, 0, 0)

        node_count = 0

        if (width and height):

            state = "move"
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "move"
            pos = Vector.add(pos, Vector(width, height, 0))
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "up"
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "lower"
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "down"
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "raise"
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "up"
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "move"
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "move"
            pos = Vector.sub(pos, Vector(width, height, 0))
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=next_id, prev=prev_id, neighbors=[])
            node_count += 1

            state = "up"
            id = cls.get_id(base_id, node_count)
            next_id = cls.get_id(base_id, node_count + 1)
            prev_id = cls.get_id(base_id, node_count - 1)
            nodes[id] = Node(id=id, state=state, pos=pos, next=None, prev=prev_id, neighbors=[])
            node_count += 1

        return nodes, head
