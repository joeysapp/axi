import random, math, time
# import opensimplex as osn

from axi.util import Console, fmap, Timer
from axi.types import Vector, Node, Sketch
 
class Generator():
    def __init__(self, *args, **kwargs):
        Console.init("generator = Generator({})\n".format(kwargs if kwargs else ""))
        self.sketches = {}

    def __repr__(self):
        return "Generator({})".format(self.__dict__)
    
    def create_sketch(self, id, *args, **kwargs) -> Sketch:
        Console.method("generator.create_sketch(id={}{})\n".format(id, kwargs if kwargs else ""))
        self.sketches[id] = Sketch(id, sketches=kwargs.get("sketches"))
        return self.sketches[id]

    def get_nodes_for_scheduler(self, id):
        if not (id in self.sketches):
            Console.error("generator.get_nodes_for_scheduler(id={}) -> {} not in self.sketches\n".format(id, id))
        else:
            Console.method("generator.get_nodes_for_scheduler(id={})\n".format(id))

            shapes = self.sketches[id].shapes
            nodes, head = self.translate_shapes_to_nodes(plot_id=id, shapes=shapes)
            Console.method("generator.get_nodes_for_scheduler(id={})".format(id))
            Console.puts("\n\t-> {}\n".format(
                Console.format("(temporary.nodes {})".format(len(nodes.keys())), ["bold", "green"])))

            return nodes, head

    """

       translate_shapes_to_nodes(plot_id, shapes, ...)

       Translates a plot's Shapes into Nodes
          * Node.pos is unchanged
          * Node.id is unchanged
          * Node.state is set (up/down/raise/lower/move/ ... wait/start/end)
    
        Removes the overhead of generating Node state elsewhere, and allows for //DYNAMIC CONTENT//
    
        It needs to do the following with a list of Shapes:
        * Start and end the Plot properly (up/down)
        * Handle shape "closing"
        * Handle shapes being connected - both the Node.next/prev, and if the pen needs to raise.
    
    
    """
    def translate_shapes_to_nodes(self, plot_id, shapes, scheduler_head=None):
        Console.method("generator.translate_shapes_to_nodes(id={}, shapes=[{} shapes], scheduler_head={})\n"
                       .format(plot_id,
                               len(shapes),
                               "None"))

        # For now, assume all sketches return to origin??
        # Otherwise, we need to know where the Scheduler's head is..
        scheduler_head = None
        head_node = None
        next_node = None
        prev_node = None
        nodes = {}

        debug = False

        shape_idx = 0
        for shape in shapes:
            shape_type = shape.type
            vertex_idx = 0
            for v in shape.vectors:

                # (plot-id)-(shape-idx)-(shape-type)-(vertex-idx)
                node_id = "{}-{}-{}-{}".format(plot_id, shape_idx, shape_type, vertex_idx)
                node_pos = Vector(0, 0, 0)
                node_state = "up"

                if (head_node == None):
                    # Beginning of Nodes
                    head_node = Node(pos=node_pos, id=node_id)
                    first_node_id = node_id
                else:
                    # head already exists -  so we need to create a new Node,
                    # set that head.next as the new Node we create, then set the head as that new node
                    tmp_next_node = Node(pos=node_pos, state=node_state, id=node_id)                    
                    
                    # if debug: print('\n0', tmp_next_node, "\t", head_node)

                    head_node.next = tmp_next_node.id

                    # if debug: print('1', tmp_next_node, "\t", head_node)

                    tmp_next_node.prev = head_node.id

                    # if debug: print('2', tmp_next_node, "\t", head_node)

                    # Do our Node creation / insertion here
                    
                    head_node = tmp_next_node
                    # set head_node.state based                
                    # if debug: print('3', tmp_next_node, "\t", head_node)                    

                vertex_idx += 1
                if (debug): print("head is now:", head_node)
                # Console.puts("Adding this head node: {}\n".format(head_node))
                nodes[node_id] = head_node
            shape_idx += 1

#        Console.method("generator.translate_shapes_to_nodes(plot_id={}, shapes=[2 shapes], scheduler_head={})\n"
#                       .format(plot_id,
#                               len(shapes),
#                               "None"))
#        Console.puts("="*80+"\n");
        Console.puts("\t-> A linked list of {} was created\n".format(
            Console.format(str(len(nodes.keys()))+" Nodes", ["bold", "green"])))

        Console.puts("\t-> The head of this linked list is: {}\n".format(
            Console.format(first_node_id, ["bold", "green"])))
        for k in nodes.keys():
            Console.puts("\t{}\n".format(nodes[k]))

        return nodes, first_node_id
            # Finishing looping through Shape's vertices.
            # Do we need to raise, or do we leave that for the next iteration?
            
