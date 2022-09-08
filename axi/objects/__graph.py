  # Python List methods

  # append, e=nd of list
  # extend, iterable to end of list
  # insert(self, index, object)
  # pop(index=-1) remove and return at index
  # remove(self, value) remove first occurrence
  # copy shallow copy of list

class Graph:
    def __init__(self, cli_args):
        origin_id = 0
        origin = Node(origin_id, state="none", pos=cli_args.pos or Vector(0, 0, 0), neighbors=[])
        self.head_id = origin_id
        self.nodes = { origin_id: origin }
        self.history = []

    def set_head(self, id):
        self.head_id = id;

    def get_head(self) -> Node:
        next_head = self.nodes[self.head_id]
        print("next_head: ", next_head.state)
        return next_head

    def add_nodes(self, nodes={}, new_graph=False):
        print("1add_nodes, nodes={} new_nodes{}".format(len(self.nodes), len(nodes)))
        if (new_graph):
            tmp_nodes = nodes.copy()
            tmp_nodes.update(self.nodes)
            self.nodes = tmp_graph
        else:
            self.nodes.update(nodes)
        print("2add_nodes, nodes={} new_nodes{}".format(len(self.nodes), len(nodes)))

            
    # note(@joeysapp): for now, a node's neighbors will likely be a single node
    def move_head_to_next_node(self):
        head = self.nodes[self.head_id]
        if (len(head.neighbors)):
           self.head_id = head.neighbors[0]
        elif head.state == 'origin':
            # End of graph:
            #   1. Go back to start of (graph item)
            #   2. Remain, raised, here
            #   3. Move back to origin
            self.head_id = "origin"

    # note(@joeysapp): Should a "graph" have a history, or should we have an State handler? 
    def extend_history(self):
        self.history.append(self.nodes[self.head_id]);
        
    def __str__(self):
        s = "Graph(head_id={} len(nodes)={} len(history)={})\n".format(self.head_id, len(self.nodes), len(self.history))
        for k in self.nodes.keys():
            s += "\t{}: {}\n".format(k, self.nodes[k])
        return s

#    def load(self, fname):
#        input_dir = "../plots/"
#        for _fname in os.listdir(input_dir):
#            print("graph.load", _fname);
#        with open(fname, "r") as file:
#            while True:
#                
#            t = file.readlines() # reads in a line at a single time, context switch prob takes forever
#            _graph_text = .split("\n")
#            path_entries = []
#            for entry_text in t_list:
#                new_entry = PathEntry(text=entry_text)
#                path_entries.append(new_entry)
#            self.path_entries.extend(path_entries)
#    
#    def save(self):
#        fname = "{}-{}.txt".format(round(time.clock_gettime(0)), len(self.path_entries))
#        with open(fname, "w") as f:
#            f.write(self.get_path_as_string())
#            f.close()
