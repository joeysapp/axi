from ..node import Node

from axi.math import Vector

class Square():
    @classmethod
    def get_id(cls, base, id):
        return "{}-{}".format(base, id)
    
    @classmethod
    def get(cls, *args, **kwargs):
#        for key in kwargs:
#           self.__setattr__(key, kwargs[key])

        base_id = kwargs.get('id')

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
            nodes[id] = Node(id=id, state=state, pos=pos, next=1, prev=None, neighbors=[])
            node_count += 1

            state = "move"
            pos = Vector.add(pos, Vector(width, height, 0))
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=2, prev=0, neighbors=[])
            node_count += 1

            state = "up"
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=3, prev=1, neighbors=[])
            node_count += 1

            state = "lower"
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=4, prev=2, neighbors=[])
            node_count += 1

            state = "down"
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=5, prev=3, neighbors=[])
            node_count += 1

            state = "raise"
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=6, prev=4, neighbors=[])
            node_count += 1

            state = "up"
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=7, prev=5, neighbors=[])
            node_count += 1

            state = "move"
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=8, prev=6, neighbors=[])
            node_count += 1

            state = "move"
            pos = Vector.sub(pos, Vector(width, height, 0))
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=9, prev=7, neighbors=[])
            node_count += 1

            state = "up"
            id = cls.get_id(base_id, node_count)
            nodes[id] = Node(id=id, state=state, pos=pos, next=None, prev=8, neighbors=[])
            node_count += 1



        return nodes, head
