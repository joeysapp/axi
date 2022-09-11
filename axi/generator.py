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
        debug = True

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
        tmp_node = None

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
                    tmp_node = Node(pos=new_pos, id=new_id, state=new_state)                    
                    if debug: print('\n( 00 - creating tmp_node )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)

                    head_node.next = tmp_node.id
                    if debug: print('\n( 01 - setting head.next = tmp )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)

                    tmp_node.prev = head_node.id
                    if debug: print('\n( 02 - setting tmp.prev = head )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)

                    # Do our Node creation / insertion here
                    if debug: print('\n( 03 - about to insert transition nodes )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)
                    new_nodes, head_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node)
                    if debug: print('\n( 04 - back inside loop = head )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)
                    
                    head_node = tmp_node
                    # set head_node.state based                
                    # if debug: print('3', tmp_node, "\t", head_node)                    

                vertex_idx += 1
                # if (debug): print("head is now:", head_node)
                # Console.puts("Adding this head node: {}\n".format(head_node))
                new_nodes[new_id] = head_node
                if debug: print('\n( !! new shape !! )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)

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
            

    """
       Called in get_sketch_as_linked_list

       Inserts required "transition" Nodes with requisite NodeStates and positions
       NodeState is a .types.enum with nice utility functions used here

    """
    def insert_transition_nodes(self, nodes, head_node, tmp_node) -> (dict, Node):
        # head_node is None, add
        <insert 7 nodes>
        # self.goto_and_lower() -> 7 Nodes

        # head_node.pos != tmp_node.pos and "same shape"
        <insert move to tmp_node.pos>
        # self.goto() -> 1 Node

        # head_node.pos != tmp_node.pos and "different shape"
        <insert 9 nodes>
        # self.raise_and_goto() -> 9 Nodes

        return nodes, tmp_node
