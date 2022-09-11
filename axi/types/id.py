"""
   NEEDS TO BE IMPLEMENTED.






   Ids are extended to SketchId, ShapeId and NodeId.

   They are how we store

   Simple creation
   
   Future ideas: 
   * Fast access and identification for Selector/Modifier

"""
import itertools

class Graph(dict):
    # Implement custom dict for the Scheduler to use
    # Implement custom dict for the Generator to use
    
    # Utility for Selector/Modifier?
    # "NodeGraph, please give me all the Nodes that look like XYZ."


class NodeId:
    global_node_count = 0

    @classmethod
    def add_node(self) -> None:
        self.global_node_count += 1

    def __init__(self, sketch_id, shape_idx, shape_type, vertex_idx):
        self.add_node()
        _id_0 = self.global_node_count

        _id_1 = sketch_id
        _id_2 = shape_idx # Which
        _id_3 = shape_type
        _id_4 = vertex_idx # Num of vertex inside shape


    def __str__(self):
        return None
