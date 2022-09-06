class Node:
    def __init__(self, id=-1, state=None, pos=None, next=None, prev=None, neighbors=[]):
        self.id = id
        self.state = state
        self.pos = pos
        self.next = next
        self.prev = prev
        self.neighbors = neighbors

    def __str__(self):
        return "{},{},{},{},{},{}".format(self.id, self.state, self.pos, self.prev, self.next, self.neighbors)
