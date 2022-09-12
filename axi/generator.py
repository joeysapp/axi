import random, math, time
# import opensimplex as osn

from axi.util import Console, fmap, Timer

from axi.types import Vector, Node, Sketch, NodeState, TypeId
 
class Generator():
    def __init__(self, *args, **kwargs):
        # Console.init("Generator({})\n".format(kwargs if kwargs else ""))
        self.sketches = {}

    def __repr__(self):
        return "Generator({})".format(self.__dict__)
    
    def create_sketch(self, name, *args, **kwargs) -> None:
        Console.method("generator.create_sketch({})\n".format(name, kwargs if kwargs else ""))

        sketches_to_append = kwargs.get("sketches")
        new_sketch = Sketch(name, sketches=sketches_to_append)

        # todo(@joeysapp): Implement custom container for Nodes
        new_sketch_key = new_sketch.id.hash

        self.sketches[new_sketch_key] = new_sketch
        return self.sketches.get(new_sketch_key
)

    def get_sketch(self, name) -> Sketch:
        return self.sketches.get(id)

    def get_sketch_as_linked_list(self, name) -> (dict, str):
        """
        * Transforms a Sketch into a linked_list of Nodes:
        - Start, perform and finish necessary serial commands
        - Handles movement for "connected" Shapes
        - [?] - Handles closing Shapes - config?
        
        returns { nodes }, head
        """
        Console.method("generator.get_sketch_as_linked_list({})\n".format(name))
        debug = True

        sketch = self.sketches.get(name)
        Console.method("The shapes look like: {}\n".format(Console.list(sketch.shapes)))

        head_node = None
        prev_node = None

        new_state = None
        new_head = None
        new_nodes = {}
        first_node_id = None
        tmp_node = None

        shape_idx = 0
        for shape in sketch.shapes:
            vector_idx = 0

            # Use this to determine whether or not the next node is the same shape or not
            shape_id = shape.id.shape_id
            # print(shape.id.__dict__, shape.id.shape_id)

            if debug:
                print('========================================================== !! NEW SHAPE ================')
                print('\t0 - Begin sketch.shapes[{}] with shape_id= {} = \n{}'.format(shape_idx, shape_id, shape))
            for v in shape.vectors:
                new_pos = Vector(v.x, v.y, v.z)
                if debug: print('\t1 - Begin sketch.shapes[{}].vectors[{}] , new_pos is {}'.format(shape_idx, vector_idx, Console.format(new_pos, ["green", "bold"])))
                if (head_node == None):
                    if debug: print('\t1b - head = None, creating tmp and starting sketch')
                    # Create new node at 0 0 set to up, move to new pos and lower
                    new_nodes, head_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node, shape_id, pos=new_pos)
                    first_node_id = head_node.id.hash
                else:
                    print('\t1a - head exists, creating tmp and calling helper fn')
                    tmp_node = Node(shape_id, pos=new_pos)
                    head_node.next = tmp_node.id.hash
                    tmp_node.prev = head_node.id.hash

                    # Do our Node creation / insertion here
                    new_nodes, tmp_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node, shape_id)

                    print('\t=== SETTING HEAD = TMP, onto next Vector (or Shape) ===')
                    head_node = tmp_node
                    new_nodes[head_node.id.hash] = head_node


                if debug: print('\t2 - End of sketch.shapes[{}].vectors[{}]'.format(shape_idx, vector_idx))
                vector_idx += 1
            if debug: print('\t3 - End of sketch.shapes[{}] (no more vectors)'.format(shape_idx))

            # This should only increment if head.next still has
            #TypeId.increment_shape_pointer()

        # End of sketch, move -> raise -> goto 0 0
        new_nodes, head_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node, shape_id)

        Console.puts("\n")
        Console.puts("\t-> A linked list of {} was created\n".format(
            Console.format(str(len(new_nodes.keys()))+" Nodes", ["bold", "green"])))
        Console.puts("\t-> The head of this linked list is: {}\n".format(
            Console.format(first_node_id, ["bold", "green"])))

        idx = 0
        for k in new_nodes.keys():
            Console.puts("\t{:2n} {}\n".format(idx, new_nodes[k]))
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
    def insert_transition_nodes(self, new_nodes, head_node, tmp_node, shape_id, **kwargs) -> (dict, Node):
        Console.method("{} generator.insert_transition_nodes(\n\tshape_id={}\n\tsize(new_nodes)={}\n\thead={}\n\ttmp= {}{})\n\n"
                       .format(
                               Console.format("[START]", ["bold", "bg-green"]),
                               shape_id,
                               len(new_nodes.keys()),
                               head_node,
                               tmp_node,
                               Console.format("\n\tkwargs={}".format(kwargs) if kwargs else "", ["blue"])
                               ))
        transition_nodes = {}
        if (head_node == None):
            print("[transition] head_node == None; shape_id={}".format(shape_id))

            node0 = Node(shape_id, pos=Vector(0, 0, 0),   state=NodeState.up                         )
            node1 = Node(shape_id, pos=Vector(0, 0, 0),   state=NodeState.move,    prev=node0.id.hash)
            node2 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.move,    prev=node1.id.hash)
            node3 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.up,      prev=node2.id.hash)
            node4 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.descend, prev=node3.id.hash)
            node5 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.down,    prev=node4.id.hash)
            node6 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.move,    prev=node5.id.hash)

            # For the sake of argument, assume we'll be moving to truly hashable IDs (and not just indiceses)
            node0.set_next(node1.id.hash)
            node1.set_next(node2.id.hash)
            node2.set_next(node3.id.hash)
            node3.set_next(node4.id.hash)
            node4.set_next(node5.id.hash)
            node5.set_next(node6.id.hash)
            # A nice NodeContainer method for this?
            new_nodes.update({
                node0.id.hash: node0,
                node1.id.hash: node1,
                node2.id.hash: node2,
                node3.id.hash: node3,
                node4.id.hash: node4,
                node5.id.hash: node5,
                node6.id.hash: node6,
            })
            # Tmp_node will be set to head outside of this function
            tmp_node = node6
        # head_node.pos != tmp_node.pos and "same shape"
        elif (head_node.pos != tmp_node.pos and head_node.id.shape_id == tmp_node.id.shape_id):
            print("\t[transition] within same Shape but head.pos != tmp.pos, set tmp.state to move");

            # print("\thead_node.id = {}".format(head_node.id.__dict__))
            # print("\ttmp_node.id = {}".format(tmp_node.id.__dict__))

            # We actually made tmp_node outside this loop (instantiated so the outside head node can get .next, .prev, etc.
            # So we just need to do this:
            tmp_node.set_state(NodeState.move)
            tmp_node = tmp_node
        # head_node.pos != tmp_node.pos and "different shape"
        elif (head_node.pos != tmp_node.pos and head_node.id.shape_id != tmp_node.id.shape_id):
            print("\t[transition] new shape and new post, so move->down->ascend->up->move->move->up->descend->down->move ")
            # not sure about this
            print("\t[transition] head is the previous shape, but it didn't know it could end.")


            node0 = Node(shape_id, pos=head_node.pos,   state=NodeState.ascend,   prev=tmp_node.id.hash)
            node1 = Node(shape_id, pos=head_node.pos,   state=NodeState.up    ,   prev=node0.id.hash    )
            node2 = Node(shape_id, pos=head_node.pos,   state=NodeState.move,     prev=node1.id.hash    )
            node3 = Node(shape_id, pos=tmp_node.pos ,   state=NodeState.move,     prev=node2.id.hash    )
            node4 = Node(shape_id, pos=tmp_node.pos,    state=NodeState.up,       prev=node3.id.hash    )
            node5 = Node(shape_id, pos=tmp_node.pos,    state=NodeState.descend,  prev=node4.id.hash    )
            node6 = Node(shape_id, pos=tmp_node.pos,    state=NodeState.down,     prev=node5.id.hash    )
            node7 = Node(shape_id, pos=tmp_node.pos,    state=NodeState.move,     prev=node6.id.hash    )

            # For the sake of argument, assume we'll be moving to truly hashable IDs (and not just indiceses)

            # Force tmp_node here to be an interim Node, not the resulting head_node like normally
            tmp_node.set_state(NodeState.down)
            tmp_node.set_pos(head_node.pos)
            tmp_node.set_next(node0.id.hash)

            node0.set_next(node1.id.hash)
            node1.set_next(node2.id.hash)
            node2.set_next(node3.id.hash)
            node3.set_next(node4.id.hash)
            node4.set_next(node5.id.hash)
            node5.set_next(node6.id.hash)
            node6.set_next(node7.id.hash)

            # A nice NodeContainer method for this?
            new_nodes.update({
                tmp_node.id.hash: tmp_node,
                node0.id.hash: node0,
                node1.id.hash: node1,
                node2.id.hash: node2,
                node3.id.hash: node3,
                node4.id.hash: node4,
                node5.id.hash: node5,
                node6.id.hash: node6,
                node7.id.hash: node7,
            })

            print("0 tmp node is now: ", tmp_node)
            print("0 node0 is now: ", node0)

            # Tmp_node will be set to head outside of this function
            tmp_node = node7

            print("1 tmp node is now: ", node7)
            # return new_nodes, node6

        elif (head_node.next == None):
            print("\t[transition] end of sketch SO move->raise->up @ head, goto home because head.next == None")
            node0 = Node(shape_id, pos=head_node.pos,   state=NodeState.down,    prev=head_node.id.hash)
            node1 = Node(shape_id, pos=head_node.pos,   state=NodeState.ascend,  prev=node0.id.hash    )
            node2 = Node(shape_id, pos=head_node.pos,   state=NodeState.up,      prev=node1.id.hash    )
            node3 = Node(shape_id, pos=head_node.pos,   state=NodeState.move,    prev=node2.id.hash    )
            node4 = Node(shape_id, pos=Vector(0, 0, 0), state=NodeState.move,    prev=node3.id.hash    )
            node5 = Node(shape_id, pos=Vector(0, 0, 0), state=NodeState.up,      prev=node4.id.hash    )

            # For the sake of argument, assume we'll be moving to truly hashable IDs (and not just indiceses)
            head_node.set_next(node0.id.hash)
            node0.set_next(node1.id.hash)
            node1.set_next(node2.id.hash)
            node2.set_next(node3.id.hash)
            node3.set_next(node4.id.hash)
            node4.set_next(node5.id.hash)

            # A nice NodeContainer method for this?
            new_nodes.update({
                node0.id.hash: node0,
                node1.id.hash: node1,
                node2.id.hash: node2,
                node3.id.hash: node3,
                node4.id.hash: node4,
                node5.id.hash: node5,
            })

            # Tmp_node will be set to head outside of this function
            tmp_node = node5
            # return new_nodes, node6
            

        else:
            print(" weird final case idk about ")

        Console.method("{} generator.insert_transition_nodes(\n\tsize(new_nodes)={}\n\thead={}\n\ttmp= {}{})\n\n"
                       .format(
                               Console.format("[END]", ["bold", "bg-red"]),
                               len(new_nodes.keys()),
                               head_node,
                               tmp_node,
                               Console.format("\n\tkwargs={}".format(kwargs) if kwargs else "", ["blue"])
                               ))

        # Tmp_node will be set to head outside of this function
        return new_nodes, tmp_node
