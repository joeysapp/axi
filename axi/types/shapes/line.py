import math

def line(params, *args, **kwargs):
    xylist = []
    if (params.length and params.pos):
        if type(params.pos) == list:
            p1 = [params.pos[0], params.pos[1]]
        else:
            p1 = [params.pos.x, params.pos.y]

        rx = 1
        ry = 0
        # ... If this is called w/o degrees, just a straight line? 
        # ... What about params like,  "x_length", lol
        
        # Avoid calling this if possible
        # todo(@joeysapp): find a fast math lib

        if (params.degrees):
            radians = (params.degrees / 180) * math.pi
            rx = math.cos(radians)
            ry = math.sin(radians)

        p2x = p1[0] + params.length * rx
        p2y = p1[1] + params.length * ry
        p2 = [p2x, p2y]
    return [p1, p2]

#class line():
#    # class method = good? = bad?
#    @classmethod
#    def get(cls, params):
#        print("shapes/line.py class method get")
#        return vertices
#
#    def __init__(self):
#        print("shapes/line.py init")
#        return vertices
