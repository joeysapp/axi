from axi.util import Console

#class Scheduler(dict):
class Scheduler():
    def __init__(self, *args, **kwargs):
        # Making our Scheduler a dictionary type?
        # super(Scheduler, self).__init__(*args, **kwargs)

        # Console.init("scheduler = Scheduler({})\n".format(kwargs))
        self.head = None      # id
        self.nodes = {}       # map of all Nodes, { id: node }
        self.queue = []       # stack of heads to print in the future, sent from Generator
        self.prev = []        # list of ids of Nodes that have been printed

        # Hopefully take this out after Generator is 100%
        # self.physical_bounds = Rect({ pos=v(0, 0, 0), width=431.8, height=279.4 });


    # Conditions the plotter needs to send a serial command:
    #   head        next   g     cmd
    #   ======================================
    #   up A        move A       goto(A) <--- this is starting condition.. matters with rel/abs decision
    #   move A      move C       goto(C)  <--- we never move on down? move? because down always goes to move first
    #   pendown     up A         lower A
    #   penup       down A       raise A
    def get_serial_command(self):
        Console.method("scheduler.get_serial_command()")

        head_node = self.nodes.get(self.head)
        next_node = self.nodes.get(head_node.next) if head_node.next in self.nodes else None

        command = None
        pos = None

        if (head_node and next_node):
            head_state = head_node.state
            next_state = next_node.state
            head_pos = head_node.pos
            next_pos = next_node.pos
            
            # Starting cond: If next is a new position, and head is currently stationary in up pos. 
            # Maybe should have a state of "starting" or something? 
            if (head_pos != next_pos and (head_state.is_up() and next_state.is_moving())):
                command = "goto"                
                pos = head_pos

            # Head/next are both in move state. Might be same pos (0, 0, 0) but just to make sure.
            elif (head_pos != next_pos and head_state.is_moving() and next_state.is_moving()):
                command = "goto"
                pos = next_pos

            # Same location, up -> lower
            if (head_pos == next_pos and (head_state.is_up() and next_state.is_lowering())):
                command = "pendown"
                pos = head_pos

            # Same location, down -> raise
            if (head_pos == next_pos and (head_state.is_down() and next_state.is_raising())):
                command = "penup"        
                pos = head_pos

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



    # todo(@joeysapp):
    # Generator should prob handle bounds and pen state during linked list creation.
    # Depends if we're gonna be modifying the resulting Nodes or not, I guess

    def is_head_within_physical_bounds(self) -> bool:
        return True

        Console.method("scheduler.is_head_within_physical_bounds({})".format(self.physical_bounds))
        pos = self.nodes[self.head].pos

        in_bounds = self.physical_bounds.contains(pos)
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

        if (head): self.queue.append(head)
        Console.puts("\n\t   {}\n\t-> {}\n".format(
            Console.format("(scheduler.queue "+str(max(0, len(self.queue)-1))+")", ["gray-0", "italic"]),
            Console.format("(scheduler.queue "+str(len(self.queue))+")", ["green", "bold"])))

    def pop_queue_to_head(self) -> None:
        Console.method("scheduler.pop_queue_to_head()")
        if (self.head != None):
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
        h = len(self.prev)
        q = len(self.queue)
        return "{}\n\t{}\n\t{}".format(
            Console.format("(scheduler.nodes "+str(n)+")", ["orange", "italic"]),
            Console.format("(scheduler.queue "+str(q)+")", ["bold", ""] if q > 0 else ["gray-0", "italic"]),
            Console.format("(scheduler.prev "+str(h)+")", ["gray-0", "italic"]))
        
    def get_graph_state(self) -> str:
        head = None if not self.head or not self.nodes else self.nodes[self.head]
        prev = None if (not head or not head.prev) else self.nodes[head.prev]
        next = None if (not head or not head.next) else self.nodes[head.next]

        # return "\t<- prev = {}\n\thead =    {}\n\t-> next = {}".format(prev, head, next)
        return "\t{}{}\n\t{}{}\n".format(
            Console.format("head = ", "orange"), Console.format(head, "orange"),
            Console.format("next = ", "gray-0"), Console.format(next, "gray-0"))
            #Console.format("prev = ", "gray-0"), Console.format(prev, "gray-0"),

    def __repr__(self) -> str:
        return "scheduler state:\n\t{}\n\n{}".format(self.get_graph_size(), self.get_graph_state())
