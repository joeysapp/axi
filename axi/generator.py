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

        new_state = None
        new_head = None
        new_nodes = {}
        first_node_id = None
        tmp_node = None

        shape_idx = 0
        for shape in sketch.shapes:
            shape_type = shape.type # ShapeType enum
            vertex_idx = 0
            is_new_shape = True

            for v in shape.vectors:
                x = v[0]
                y = v[1]
                new_pos = Vector(x, y, 0)
                # (sketch_id)-(relative_node_count)-(shape_idx)-(shape_type)-(vertex_idx)
                new_id = "{}-{}-{}-{}".format(id, shape_idx, shape_type, vertex_idx)

                if (head_node == None):
                    if debug: print('\n( 0 - head = None, creating tmp_node and starting sketch )\nhead=', head_node, "\ntmp =", tmp_node)

                    # Start of sketch
                    # Create node at 0 0 set to up, move to new pos and lower.
                    new_nodes, head_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node, id=new_id, pos=new_pos)
                    first_node_id = head_node.id
                else:
                    # head already exists -  so we need to create a new Node,
                    # set that head.next as the new Node we create, then set the head as that new node
                    tmp_node = Node(pos=new_pos, id=new_id, state=new_state)                    
                    # if debug: print('\n( 00 - creating tmp_node )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)

                    head_node.next = tmp_node.id
                    # if debug: print('\n( 01 - setting head.next = tmp )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)

                    tmp_node.prev = head_node.id
                    # if debug: print('\n( 02 - setting tmp.prev = head )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)

                    # Do our Node creation / insertion here
                    # if debug: print('\n( 03 - about to insert transition nodes )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)
                    new_nodes, head_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node)
                    # if debug: print('\n( 04 - back inside loop = head )\n\ttmp_node=', tmp_node, "\n\thead_node=", head_node)
                    
                    head_node = tmp_node
                    # set head_node.state based                
                    # if debug: print('3', tmp_node, "\t", head_node)                    

                vertex_idx += 1
                # if (debug): print("head is now:", head_node)
                # Console.puts("Adding this head node: {}\n".format(head_node))
                new_nodes[new_id] = head_node
                if debug: print('\n( {} end vertex loop !! )\nhead= '.format(len(new_nodes.keys())), head_node, "\ntmp =", tmp_node)
                is_new_shape = False
            if debug: print('\n( {} end shape loop !! )\nhead= '.format(len(new_nodes.keys())), head_node, "\ntmp =", tmp_node)
            shape_idx += 1

        # End of sketch, move -> raise -> goto 0 0
        new_nodes, head_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node)

        Console.puts("\n")
        Console.puts("\t-> A linked list of {} was created\n".format(
            Console.format(str(len(new_nodes.keys()))+" Nodes", ["bold", "green"])))
        Console.puts("\t-> The head of this linked list is: {}\n".format(
            Console.format(first_node_id, ["bold", "green"])))

        idx = 0
        for k in new_nodes.keys():
            Console.puts("\t{} {}\n".format(idx,new_nodes[k]))
            idx += 1

        exit()
        return new_nodes, first_node_id
            # Finishing looping through Shape's vertices.
            # Do we need to raise, or do we leave that for the next iteration?
            

    """
       Called in get_sketch_as_linked_list

       Inserts required "transition" Nodes with requisite NodeStates and positions
       NodeState is a .types.enum with nice utility functions used here

    """
    def insert_transition_nodes(self, nodes, head_node, tmp_node, **kwargs) -> (dict, Node):
        Console.method("generator.insert_transition_nodes({}\nhead={}\ntmp= {})\n".format(len(nodes.keys()), head_node, tmp_node))
        # head_node is None, add
        # self.goto_and_lower() -> 7 Nodes
        if (head_node == None):
            print("self.goto_and_lower")
            # Create/update IDs
            # There is no head_node, so node0 will be head
            node0 = Node(pos=Vector(0, 0, 0),   state=NodeState.up)
            node1 = Node(pos=Vector(0, 0, 0),   state=NodeState.move)
            node2 = Node(pos=kwargs.get("pos"), state=NodeState.move)
            node3 = Node(pos=kwargs.get("pos"), state=NodeState.up)
            node4 = Node(pos=kwargs.get("pos"), state=NodeState.descend)
            node5 = Node(pos=kwargs.get("pos"), state=NodeState.down)
            node6 = Node(pos=kwargs.get("pos"), state=NodeState.move)
            nodes.update(....)
            return new_nodes, node6

        # head_node.pos != tmp_node.pos and "same shape"
        # self.goto() -> 1 Node
        elif (head_node.pos != tmp_node.pos and head_node.id.shape_id == tmp_node.id.shape_id):
            print(" same shape, move");
            node0 = Node(pos=tmp_node.pos, state=NodeState.move)
            new_nodes.populate_container_method(node0)
            return new_nodes, node0
        
        # head_node.pos != tmp_node.pos and "different shape"
        # self.raise_and_goto() -> 9 Nodes
        elif (head_node.pos != tmp_node.pos and head_node.id.shape_id != tmp_node.id.shape_id):
            print(" different shape, raise, goto tmp, down tmp")

        elif (head_node.next == None):
            print(" end of sketch, move->raise at head, goto home.")

        else:
            print(" weird final case idk about ")

        return nodes, tmp_node
