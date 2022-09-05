
class Scheduler:
    def __init__(self, args):
        Console.log("Scheduler.__init__(args={})\n".format(args))
        self.head = None    # Node
        self.nodes = {}     # map of all Nodes
        self.queue = []     # queue of Generators
        self.history = []   # list of Generators that have been printed
