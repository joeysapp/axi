

     def __init__(self, args):
        Console.log("Generator.__init__(args={})\n".format(args))
        osn.seed(42)

    def get_random(self, head, bounds):
        Console.log("Generator.get_random(head={}, bounds={})\n".format(head, bounds))
        nodes = {}
        node = head;

        amt = 100;
        for i in range(0, amt):
            id = node.id + 1
            pos = node.pos

            n = fmap(random.random(), 0, 1, 0, math.pi*2)

            t = i/10.0
            t = math.sin(t);
            print("t = {}".format(t))
            m = 0.9 + t

            nx = pos.x + m * math.cos(n) # x is technically the vertical component
            ny = pos.y + m * math.sin(n) # y is techincally the horizontal component
            action = "move"
            if (node.action == "finish" or node.action == "none" or action == "raise"):
                action = "lower"
            elif (i == amt-1):
                action = "finish"

            if (nx <= bounds["min"]["x"] or nx >= bounds["max"]["x"]):
                node = Node(id=id, pos=Vector(pos.x, pos.y, pos.z), action='raise', neighbors=[id+1])
                nodes[id] = node
                id = id + 1
                nx = random.randrange(bounds["min"]["x"], bounds["max"]["x"])
            if (ny <= bounds["min"]["y"] or ny >= bounds["max"]["y"]):
                node = Node(id=id, pos=Vector(pos.x, pos.y, pos.z), action='raise', neighbors=[id+1])
                nodes[id] = node
                id = id + 1
                ny = random.randrange(bounds["min"]["y"], bounds["max"]["y"])

            node = Node(id=id, pos=Vector(nx, ny, pos.z), action=action, neighbors=[id+1])
            nodes[id] = node

            
        return { "id": head.id + 1, "nodes": nodes }


    
    def _next_simplex_fun(self, path_entry) -> PathEntry:
        # self._generator....
        print('objects/generator/next')
        ## creative part 
        x = path_entry.pos.x;
        y = path_entry.pos.y;
        z = path_entry.pos.z;
        ndiv = 16.
        t = path_entry.time / 1000000.;
        n = osn.noise3(x/ndiv, y/ndiv, 0)
        print('\t 001 n =', n, end='\n')
        n = map(n, -1, 1, 0, math.pi * 2)

        path_entry.vel.mult(0.95)

        path_entry.acc = Vector(math.cos(n), math.sin(n), 0.0)
        path_entry.acc.limit(1);
        path_entry.vel.limit(1)

        ## end creative part
        next_vel = path_entry.vel.add(path_entry.acc)
        next_pos = path_entry.pos.add(path_entry.vel)

        if (next_pos.x > 66 or next_pos.x < 33):
            next_pos.x = 33 + random.random()*33.
            next_pos.y = random.random()*225

            next_vel = Vector(0, 0, 0)
        if (next_pos.y > 225 or next_pos.y < 0):
            next_pos.x = 33 + random.random()*33.0
            next_pos.y = random.random()*225
            next_vel = Vector(0, 0, 0)

        time = path_entry.time + 1
        # pen_pos = path_entry.pen_pos
        next_path_entry = PathEntry(pos=next_pos, vel=next_vel, acc=Vector(0, 0, 0), time=time)
        return next_path_entry;

