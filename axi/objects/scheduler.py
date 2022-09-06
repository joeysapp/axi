from axi.util import Console

class Scheduler:
    def __init__(self, args):
        Console.log("Scheduler.__init__(args={})\n".format(args))
        self.head = None    # Node
        self.nodes = {}     # map of all Nodes, { id: node }
        self.stack = []     # stack of Generators
        self.history = []   # list of ids of (head) Nodes that have been printed


    # Conditions the plotter needs to send a serial command:
    #   head        next        cmd
    #   ======================================
    #   up A        move A       goto(A)
    #   move A      move C       goto(C)
    #   pendown     up A         lower A
    #   penup       down A       raise A
    def get_serial_command(self, node, next_node):
        Console.log("!!!!!!! not implemented Scheduler.get_serial_command({}, {})".format(node, next_node))
        
        return None;
