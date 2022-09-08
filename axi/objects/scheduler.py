from axi.util import Console

class Scheduler:
    def __init__(self, *args, **kwargs):
        Console.init("scheduler = Scheduler({})\n".format(kwargs))
        self.head = None    # Node
        self.nodes = {}     # map of all Nodes, { id: node }
        self.waiting_heads = []     # stack of heads to print in the future
        self.history = []   # list of ids of (head) Nodes that have been printed

    def __repr__(self) -> str:
        return "Scheduler({})".format(self.__dict__)

    # Conditions the plotter needs to send a serial command:
    #   head        next        cmd
    #   ======================================
    #   up A        move A       goto(A) <--- this is starting condition.. matters with rel/abs decision
    #   move A      move C       goto(C)  <--- we never move on down? move? because down always goes to move first
    #   pendown     up A         lower A
    #   penup       down A       raise A
    def get_serial_command_for_plotter(self):
        Console.method("scheduler.get_serial_command_for_plotter()\n")

        head = self.nodes[self.head]
        next = self.nodes[head.next] if head.next in self.nodes else None

        command = None
        pos = None

        Console.method("\t\thead={}\n".format(head))
        Console.method("\t\tnext={}\n".format(next))
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
        Console.method("scheduler.get_travel_distance() -> {}\n".format(distance))
        return distance

    def is_head_within_bounds(self, bounds) -> bool:
        is_within_bounds = True
        pos = self.nodes[self.head].pos
        if (pos.x < bounds["min"]["x"] or pos.x > bounds["max"]["x"]):
            is_within_bounds = False
        if (pos.y < bounds["min"]["y"] or pos.y > bounds["max"]["y"]):
            is_wthin_bounds = False
        Console.method("scheduler.is_head_within_bounds({}) -> {}\n".format(bounds, "True" if is_within_bounds else "False"))
        return is_within_bounds

    def add_nodes(self, nodes) -> None:
        Console.method("scheduler.add_nodes({})\n".format(Console.list(nodes)))
        self.nodes.update(nodes)

    def traverse_linked_list(self) -> None:
        Console.method("scheduler.traverse_linked_list(head={}))\n".format(self.head))
        if not self.head == None:
            self.head = self.nodes[self.head].next

    def append_waiting_heads(self, head) -> None:
        Console.method("scheduler.append_waiting_heads(id={})\n".format(head))
        self.waiting_heads.append(head)

    def pop_waiting_heads(self) -> None:
        Console.method("scheduler.pop_waiting_heads(): head: {} -> ... \n".format(self.head))
        if (self.head != None and self.head.next == None):
            self.head.next = next_head
        self.head = self.waiting_heads.pop()
        Console.method("scheduler.pop_waiting_heads(): head: {}\n".format(self.head))
