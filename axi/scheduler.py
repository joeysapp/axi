from axi.util import Console
from axi.types import Bounds

class Scheduler(dict):
    def __init__(self, *args, **kwargs):
        # Making our Scheduler a dictionary type?
        super(Scheduler, self).__init__(*arg, **kwargs)

        Console.init("scheduler = Scheduler({})\n".format(kwargs))
        self.head = None      # id
        self.nodes = {}       # map of all Nodes, { id: node }
        self.queue = []       # stack of heads to print in the future, sent from Generator
        self.prev = []        # list of ids of Nodes that have been printed

        # Hopefully take this out after Generator is 100%
        self.bounds = Bounds()


    # Conditions the plotter needs to send a serial command:
    #   head        next   g     cmd
    #   ======================================
    #   up A        move A       goto(A) <--- this is starting condition.. matters with rel/abs decision
    #   move A      move C       goto(C)  <--- we never move on down? move? because down always goes to move first
    #   pendown     up A         lower A
    #   penup       down A       raise A
    def get_serial_command(self):
        Console.method("scheduler.get_serial_command()")

        head = self.nodes[self.head]
        next = self.nodes[head.next] if head.next in self.nodes else None

        head_node = self.nodes.get(self.head)

        command = None
        pos = None
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

            #if command:
            #    Console.method("\t->{} {}\n".format(command, pos if pos else "None"))

    
        color = "green" if command else "gray-0"
        cmd_str = "\"" + str(command) + "\"" if command else "None"
        Console.puts("\n\t-> {}, {}\n".format(
            Console.format(cmd_str, [color, "bold" if command else "italic"]),
            Console.format(pos, [color, "italic"])))

        return command, pos




    # Should Nodes themselves know their distance? ... weighted edges...
    def get_travel_distance(self):
        p1 = self.nodes[self.head]
        p2 = self.nodes[p1.next]

        distance = p1.pos.dist(p2.pos)
        Console.method("scheduler.get_travel_distance() -> {}\n".format(distance))
        return distance

    # Hopefully take this out after Generator is complete
    def is_head_within_bounds(self) -> bool:
        Console.method("scheduler.is_head_within_bounds({})".format(bounds))
        pos = self.nodes[self.head].pos
        in_bounds = self.bounds.check(pos)
        Console.puts("\n\t-> {}\n".format(
            Console.format("True", ["bold", "green"])
            if in_bounds else
            Console.format("False", ["red", "italic"])))

        return in_bounds

    def add_nodes(self, nodes) -> None:
        # Console.method("scheduler.add_nodes({})\n".format(Console.list(nodes)))
        Console.method("scheduler.add_nodes(({} nodes))\n".format(len(nodes.keys())))
        l = len(self.nodes.keys())
        Console.puts("\t   {}".format(
            Console.format("(scheduler.nodes "+str(len(self.nodes.keys()))+")", ["gray-0" if l == 0 else "green", "italic"])))

        self.nodes.update(nodes)
        Console.puts("\n\t-> {}".format(
            Console.format("(scheduler.nodes "+str(len(self.nodes.keys()))+")\n", ["green", "bold"])))



    def goto_next_node(self) -> None:
        Console.method("scheduler.goto_next_node()\n")
        Console.puts("\t   {}".format(
            Console.format("head = "+str(self.head)+"\n", ["gray-0", "italic"])))

        self.prev.append(self.head)
        self.head = self.nodes[self.head].next
        Console.puts("\t-> {}".format(
            Console.format("head = "+str(self.head)+"\n", ["green" if self.head else "gray-0", "bold" if self.head else "italic"])))



    def append_to_queue(self, head) -> None:
        Console.method("scheduler.append_to_queue(head={})".format(head))

        self.queue.append(head)
        Console.puts("\n\t   {}\n\t-> {}\n".format(
            Console.format("(scheduler.queue "+str(len(self.queue)-1)+")", ["gray-0", "italic"]),
            Console.format("(scheduler.queue "+str(len(self.queue))+")", ["green", "bold"])))

    def pop_queue_to_head(self) -> None:
        Console.method("scheduler.pop_queue_to_head()")
        if (self.head != None and self.head.next == None):
            self.head.next = next_head

        Console.puts("\n\t   {}, {}".format(
            Console.format("(scheduler.queue "+str(len(self.queue))+")", ["gray-0", "italic"]),
            Console.format("head = {}".format(self.head if self.head else "None"), ["gray-0", "italic"])))

        self.head = self.queue.pop()

        Console.puts("\n\t-> {}, {}\n".format(
            Console.format("(scheduler.queue "+str(len(self.queue))+")", ["gray-0", "italic"]),
            Console.format("head = {}".format(self.head if self.head else "None"), ["green", "bold"])))



    
    def get_graph_size(self) -> str:
        n = len(self.nodes.keys())
        h = len(self.history)
        q = len(self.queue)
        return "{}\n\t{}\n\t{}".format(
            Console.format("(scheduler.nodes "+str(n)+")", ["orange", "italic"]),
            Console.format("(scheduler.queue "+str(q)+")", ["bold", ""] if q > 0 else ["gray-0", "italic"]),
            Console.format("(scheduler.history "+str(h)+")", ["gray-0", "italic"]))
        
    def get_graph_state(self) -> str:
        head = None if not self.head or not self.nodes else self.nodes[self.head]
        prev = None if (not head or not head.prev) else self.nodes[head.prev]
        next = None if (not head or not head.next) else self.nodes[head.next]

        # return "\t<- prev = {}\n\thead =    {}\n\t-> next = {}".format(prev, head, next)
        return "\t{}{}\n\t{}{}\n\t{}{}".format(
            Console.format("head = ", "orange"), Console.format(head, "orange"),
            Console.format("prev = ", "gray-0"), Console.format(prev, "gray-0"),
            Console.format("next = ", "gray-0"), Console.format(next, "gray-0"))

    def __repr__(self) -> str:
        return "scheduler state:\n\t{}\n\n{}".format(self.get_graph_size(), self.get_graph_state())
