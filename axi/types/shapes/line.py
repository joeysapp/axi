vectors = [
    [0, 0],
    [0, 1],
]

def line(args, kwargs):
    print("types/shapes/line.py being called with: args={} kwargs={}".format(args, kwargs))
    params = kwargs.get("params")

    # Param is just a dict at this point, design something later
    # because order of param op can matter

    _vectors = list(vectors)    
    _length = params.length or 1
    _vectors[1][1] *= _length
    # print("_length: "_length)

    _pos = params.pos or None
    if (_pos):
        _vectors[0][0] += _pos.x
        _vectors[1][0] += _pos.x
        _vectors[0][1] += _pos.y
        _vectors[1][1] += _pos.y

#    for k in params.__dict__:
#        v = getattr(params, k)
#        print("{} : {}".format(k, v))
#        if k == 'pos':
#            offset = v
#            for vector in _vectors:
#                vector[0] += offset.x
#                vector[1] += offset.y
#            
            
    return _vectors

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
