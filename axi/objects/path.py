# from axi.util import Console

class Path:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            print("Path.__init__: %s == %s" % (k, v))
        
        self._path = []
        # append, end of list
        # extend, iterable to end of list
        # insert(self, index, object)
        # pop(index=-1) remove and return at index
        # remove(self, value) remove first occurrence
        # copy shallow copy of list
        self._graph = []

        # self.log = Console()

    @property
    def path(self):
        return self._path
    
    
