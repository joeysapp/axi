import random, math, time
# import opensimplex as osn

from axi.util import Console, fmap, Timer

from axi.types import Node, Sketch, NodeState, TypeId, v
 
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
           Translates ordered list of Shapes (themselves lists of Vectors)
           into working linked list of Nodes with necessary pen state transitions
        """
        debug = False
        Console.method("generator.get_sketch_as_linked_list({})\n".format(name))

        sketch = self.sketches.get(name)
        new_nodes = {}
        first_node_id = None

        head_node = None
        tmp_node = None

        shape_id = None

        for shape in sketch.shapes:

            # Use this to determine whether or not the next node is the same shape or not
            shape_id = shape.id.shape_id
            vector_idx = 0

            if debug:
                print('========================================================== !! NEW SHAPE ================')
                print('\t0 - Loop of sketch.shapes with shape_id={} = \n{}'.format(shape_id, shape))
            for vec in shape.vectors:
                if debug:
                    print("new_nodes: ")
                    for key in new_nodes.keys():
                        print(new_nodes[key])
                new_pos = v(vec.x, vec.y, vec.z)

                if debug: print('\t1 - Loop of sketch.shapes with shapes[{}].vectors[{}] = {}'.format(shape_id, vector_idx, Console.format(new_pos, ["green", "bold"])))
                if (head_node == None):
                    if debug: print('\t1b - head = None, creating tmp and starting sketch')
                    # Create new node at 0 0 set to up, move to new pos and lower
                    tmp_node = Node(shape_id, pos=v(0, 0, 0), state=NodeState.up)
                    first_node_id = tmp_node.id.hash
                    new_nodes, tmp_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node, shape_id, pos=new_pos, first_node_id=first_node_id)
                else:
                    if debug: print('\t1a - head exists, make tmp and call transition fn, head is ='+str(head_node))
                    tmp_node = Node(shape_id, pos=new_pos)
                    head_node.next = tmp_node.id.hash
                    tmp_node.prev = head_node.id.hash
                    new_nodes, tmp_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node, shape_id)
                if debug: print('\t2 - End of sketch.shapes[{}].vectors[{}]'.format(shape_idx, vector_idx))
                if debug: print('\t=== SETTING HEAD = TMP, onto next Vector (or Shape) ===')
                head_node = tmp_node
                new_nodes[head_node.id.hash] = head_node
                if debug: print("\t== head is now: "+str(head_node))
                vector_idx += 1
            if debug: print('\t3 - End of sketch.shapes[{}] (no more vectors)'.format(shape_idx))

        # End of sketch, move -> raise -> goto 0 0
        if (head_node):
            new_nodes, head_node = self.insert_transition_nodes(new_nodes, head_node, tmp_node, shape_id)

        Console.puts("\n\tThe following list of Shapes were translated into a linked list: \n")
        for shape in sketch.shapes:
            Console.puts("\t{}\n".format(shape))
        Console.puts("\n\t-> A linked list of {} was created\n".format(
            Console.format(str(len(new_nodes.keys()))+" Nodes", ["bold", "green"])))
        Console.puts("\t-> The head of this linked list is: {}\n".format(
            Console.format(first_node_id, ["bold", "green"])))
        
        Console.puts("\n\t"+"="*114+"\n")

        idx = 0
        for k in new_nodes.keys():
            Console.puts("\t{}\n".format(new_nodes[k]))
            # Console.puts("\t{:2n} {}\n".format(idx, new_nodes[k]))
            idx += 1

        return new_nodes, first_node_id

    """
       Called in get_sketch_as_linked_list

       Inserts required "transition" Nodes with requisite NodeStates and positions
       NodeState is a .types.enum with nice utility functions used here

       If kwargs.pos is set (first creation) the tmp_node returned is actually the head node.

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
        debug = True
        if (head_node == None):
            if debug: print("[transition] head_node == None; shape_id={}".format(shape_id))
            node1 = Node(shape_id, pos=v(0, 0, 0),   state=NodeState.move,    prev=tmp_node.id.hash)
            node2 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.move,    prev=node1.id.hash)
            node3 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.up,      prev=node2.id.hash)
            node4 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.descend, prev=node3.id.hash)
            node5 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.down,    prev=node4.id.hash)
            node6 = Node(shape_id, pos=kwargs.get("pos"), state=NodeState.move,    prev=node5.id.hash)

            # For the sake of argument, assume we'll eventually move to truly hashable IDs (and not just indiceses)
            tmp_node.set_next(node1.id.hash)
            node1.set_next(node2.id.hash)
            node2.set_next(node3.id.hash)
            node3.set_next(node4.id.hash)
            node4.set_next(node5.id.hash)
            node5.set_next(node6.id.hash)

            # todo(@joeysapp): A nice NodeContainer method for this?
            new_nodes.update({
                tmp_node.id.hash: tmp_node,
                node1.id.hash: node1,
                node2.id.hash: node2,
                node3.id.hash: node3,
                node4.id.hash: node4,
                node5.id.hash: node5,
                node6.id.hash: node6,
            })
            tmp_node = node6

        # and -> "or" on 2022-09-14, maybe lets different shapes share pos?
        elif (head_node.pos != tmp_node.pos and head_node.id.shape_id == tmp_node.id.shape_id):
        # elif (head_node.pos != tmp_node.pos and head_node.id.shape_id == tmp_node.id.shape_id):
            if debug: print("\t[transition] head.pos != tmp.pos and head.shape_id == tmp.shape_id, so set tmp.state to move");
            # head is already in move state, so we just need to do this:
            tmp_node.set_state(NodeState.move)
            tmp_node = tmp_node

        elif (head_node.pos != tmp_node.pos and head_node.id.shape_id != tmp_node.id.shape_id):
            if debug: print("\t[transition] head is the previous shape, but it didn't know it could end.")

            # head and pos are different pos and different shape.
            # todo(@joeysapp): handle "connected" shapes in the future, consider a utility Vector.equality(head.pos, tmp.pos, DELTA)
            node0 = Node(shape_id, pos=head_node.pos,   state=NodeState.ascend,   prev=tmp_node.id.hash)
            node1 = Node(shape_id, pos=head_node.pos,   state=NodeState.up,       prev=node0.id.hash    )
            node2 = Node(shape_id, pos=head_node.pos,   state=NodeState.move,     prev=node1.id.hash    )
            node3 = Node(shape_id, pos=tmp_node.pos ,   state=NodeState.move,     prev=node2.id.hash    )
            node4 = Node(shape_id, pos=tmp_node.pos,    state=NodeState.up,       prev=node3.id.hash    )
            node5 = Node(shape_id, pos=tmp_node.pos,    state=NodeState.descend,  prev=node4.id.hash    )
            node6 = Node(shape_id, pos=tmp_node.pos,    state=NodeState.down,     prev=node5.id.hash    )
            node7 = Node(shape_id, pos=tmp_node.pos,    state=NodeState.move,     prev=node6.id.hash    )

            # Force tmp_node here to be a transition Node, *NOT* the resulting head as usual
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
            tmp_node = node7
        elif (head_node.next == None):
            if debug:
                print("\t[transition] end of sketch SO move->raise->up @ head, goto home because head.next == None")
            node0 = Node(shape_id, pos=head_node.pos,   state=NodeState.down,    prev=head_node.id.hash)
            node1 = Node(shape_id, pos=head_node.pos,   state=NodeState.ascend,  prev=node0.id.hash    )
            node2 = Node(shape_id, pos=head_node.pos,   state=NodeState.up,      prev=node1.id.hash    )
            node3 = Node(shape_id, pos=head_node.pos,   state=NodeState.move,    prev=node2.id.hash    )
            node4 = Node(shape_id, pos=v(0, 0, 0), state=NodeState.move,    prev=node3.id.hash    )
            node5 = Node(shape_id, pos=v(0, 0, 0), state=NodeState.up,      prev=node4.id.hash    )

            head_node.set_next(node0.id.hash)
            node0.set_next(node1.id.hash)
            node1.set_next(node2.id.hash)
            node2.set_next(node3.id.hash)
            node3.set_next(node4.id.hash)
            node4.set_next(node5.id.hash)

            new_nodes.update({
                node0.id.hash: node0,
                node1.id.hash: node1,
                node2.id.hash: node2,
                node3.id.hash: node3,
                node4.id.hash: node4,
                node5.id.hash: node5,
            })

            tmp_node = node5
        else:
            print(" weird final case idk about, need to impl equality of v class? or are the shape_ids not eq?")
            print("head.pos: {}".format(head_node.pos))
            print("tmp.pos: {}".format(tmp_node.pos))
            print("head_node.id: {}".format(head_node.id.shape_id))
            print("tmp_node.id: {}".format(tmp_node.id.shape_id))

            print("type(head)={}\ttpye(tmp)={}".format(type(head_node), type(tmp_node)))
            print("pos_neq={}\tshape_id_eq={}".format(head_node.pos != tmp_node.pos, head_node.id.shape_id == tmp_node.id.shape_id))
            #(head_node.pos != tmp_node.pos and head_node.id.shape_id == tmp_node.id.shape_id):

            exit()
            # print("are they equal? {}".format(tmp_node.pos == head_node.pos))

        Console.method("{} generator.insert_transition_nodes(\n\tsize(new_nodes)={}\n\thead={}\n\ttmp= {}{})\n\n"
                       .format(
                               Console.format("[END]", ["bold", "bg-red"]),
                               len(new_nodes.keys()),
                               head_node,
                               tmp_node,
                               Console.format("\n\tkwargs={}".format(kwargs) if kwargs else "", ["blue"])
                               ))

        # tmp_node will be set to head
        return new_nodes, tmp_node
