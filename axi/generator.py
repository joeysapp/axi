import random, math, time
# import opensimplex as osn

from axi.util import Console, fmap, Timer

from axi.types import Vector, Node, Sketch, NodeState
 
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

    def get_sketch_as_linked_list(self, id) -> (dict, str):
        """
        * Transforms a Sketch into a linked_list of Nodes:
        - Start, perform and finish necessary serial commands
        - Handles movement for "connected" Shapes
        - [?] - Handles closing Shapes - config?
        
        returns { nodes }, head
        """
        Console.method("generator.get_sketch_as_linked_list(id={})\n".format(id))
        debug = False

        # todo(joeysapp):
        # - Ability to insert a Sketch in the middle of already-printing Sketch?
        # - OR, leave that for now and think about the Modifier doing that.
        # scheduler_head = None                       
        sketch = self.sketches.get(id)
        Console.method("- sketch = {}\n".format(sketch))

        head_node = None
        prev_node = None

        new_head = None
        new_nodes = {}
        first_node_id = None

        shape_idx = 0
        for shape in sketch.shapes:

            shape_type = shape.type # ShapeType enum
            vertex_idx = 0

            for v in shape.vectors:

                x = v[0]
                y = v[1]
                new_pos = Vector(x, y, 0)
                new_state = NodeState.up
                # (sketch_id)-(relative_node_count)-(shape_idx)-(shape_type)-(vertex_idx)
                new_id = "{}-{}-{}-{}".format(id, shape_idx, shape_type, vertex_idx)

                if (head_node == None):
                    # Beginning of Nodes
                    head_node = Node(pos=new_pos, id=new_id, state=new_state)
                    first_node_id = new_id
                else:
                    # head already exists -  so we need to create a new Node,
                    # set that head.next as the new Node we create, then set the head as that new node
                    tmp_next_node = Node(pos=new_pos, id=new_id, state=new_state)                    
                    
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
                new_nodes[new_id] = head_node
            shape_idx += 1

        Console.puts("\n")
        Console.puts("\t-> A linked list of {} was created\n".format(
            Console.format(str(len(new_nodes.keys()))+" Nodes", ["bold", "green"])))
        Console.puts("\t-> The head of this linked list is: {}\n".format(
            Console.format(first_node_id, ["bold", "green"])))

        for k in new_nodes.keys():
            Console.puts("\t{}\n".format(new_nodes[k]))

        return new_nodes, first_node_id
            # Finishing looping through Shape's vertices.
            # Do we need to raise, or do we leave that for the next iteration?
            
