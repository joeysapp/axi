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


    # Conditions the plotter needs to send a serial command:
    #   head        next        cmd
    #   ======================================
    #   up A        move A       goto(A) <--- this is starting condition.. matters with rel/abs decision
    #   move A      move C       goto(C)  <--- we never move on down? move? because down always goes to move first
    #   pendown     up A         lower A
    #   penup       down A       raise A
    def get_serial_command_for_plotter(self):
        Console.method("Scheduler.get_serial_command_for_plotter()\n")

        head = self.nodes[self.head]
        next = self.nodes[head.next] if head.next in self.nodes else None

        command = None
        pos = None

        Console.debug("\t\thead={}\n".format(head))
        Console.debug("\t\tnext={}\n".format(next))
        if (head and next):
            head_s = head.state
            next_s = next.state
            head_p = head.pos
            next_p = next.pos
            
            # Starting cond: If next is a new position, and head is currently stationary in up pos. 
            # Maybe should have a state of "starting" or something? 
            if (head_p != next_p and (head_s == 'up' and next_s == 'move')):
                command = "goto"
                pos = head_pos

            # Head/next are both in move state. Might be same pos (0, 0, 0) but just to make sure.
            elif (head_s == 'move' and next_s == 'move'):
                command = "goto"
                pos = next_p

            # Same location, up -> lower
            if (head_p == next_p and (head_s == "up" and next_s == "lower")):
                command = "lower"
                pos = head_p

            # Same location, down -> raise
            if (head_p == next_p and (head_s == "down" and next_s == "raise")):
                command = "raise"        
                pos = head_p

            if command: Console.method("\t->{} {}\n".format(command, pos if pos else "None"))
            return command, pos
        else:
            return None, None


    def get_travel_distance(self):
        p1 = self.nodes[self.head]
        p2 = self.nodes[p1.next]

        distance = p1.pos.dist(p2.pos)
        Console.debug("get_travel_distance.Distance is : {}\n".format(distance))
        return distance

    
    def is_head_within_bounds(self, bounds) -> bool:
        is_within_bounds = True
        pos = self.nodes[self.head].pos
        if (pos.x <= bounds["min"]["x"] or pos.x >= bounds["max"]["x"]):
            is_within_bounds = False
        if (pos.y <= bounds["min"]["y"] or pos.y >= bounds["max"]["y"]):
            is_wthin_bounds = False
        return is_within_bounds
        

    def traverse_linked_list(self) -> None:
        if (self.head):            
            self.head = self.nodes[self.head].next


    def push_generator_to_stack(self, generator) -> None:
        Console.log("Scheduler.push_generator_to_stack({})\n".format(generator))
        self.stack.insert(0, generator)

    def pop_generator_stack(self) -> None:
        Console.log("Scheduler.pop_generator_stack\n")
        next_generator = self.stack.pop()

        # not sure if I like generation happening on the pop
        # Also, we need to deal with generator-to-generator creation

        # As in, are we always returning home?
        # I think just returning to where the Generator started probably is ideal?


        # If we don't pass a Generator a pos variable, do we assume it'll always be relative?

        next_nodes, next_head = next_generator.gen()

        self.nodes.update(next_nodes)
        self.history.append(next_head)
        self.head = next_head

        # taken from old main:
        #next_gen = scheduler.stack.pop()

        # Add all the new nodes to the scheduler's nodes                
        #scheduler.nodes.update(next_gen.nodes)
        #scheduler.history.append(nest_gen.id)

        # A senerator's id is the first node
        #scheduler.head = scheduler.nodes[next_gen.id]



        
