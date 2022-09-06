from axi.util import Console

class Scheduler:
    def __init__(self, *args, **kwargs):
        Console.log("Scheduler.__init__({})\n".format(kwargs))
        self.head = None    # Node
        self.nodes = {}     # map of all Nodes, { id: node }
        self.stack = []     # stack of Generators to print in future
        self.history = []   # list of ids of (head) Nodes that have been printed

    def __repr__(self) -> str:
        return "Scheduler.__repr__({})".format(self.__dict__)
        

    def push_generator_to_stack(self, generator) -> None:
        Console.log("Scheduler.push_generator_to_stack({})\n".format(generator))
        self.stack.insert(0, generator)

    def pop_generator_stack(self) -> None:
        Console.log("Scheduler.pop_generator_stack\n")
        next_generator = self.stack.pop()
        next_nodes, next_head = next_generator.gen()

        self.nodes.update(next_nodes)
        self.history.append(next_head)
        self.head = next_head

                #next_gen = scheduler.stack.pop()

                # Add all the new nodes to the scheduler's nodes                
                #scheduler.nodes.update(next_gen.nodes)
                #scheduler.history.append(nest_gen.id)

                # A senerator's id is the first node
                #scheduler.head = scheduler.nodes[next_gen.id]



        

    # Conditions the plotter needs to send a serial command:
    #   head        next        cmd
    #   ======================================
    #   up A        move A       goto(A)
    #   move A      move C       goto(C)
    #   pendown     up A         lower A
    #   penup       down A       raise A
    def get_serial_command(self, node, next_node):
        Console.log("!!!!!!! not implemented Scheduler.get_serial_command({}, {})".format(node, next_node))
        
        return "FOO", "BAR?"
