# The details of the python hash table implementation
# https://stackoverflow.com/a/13514743
#
#    def __hash__(self):
#        print("TypeId.__hash__({}) -> {}".format(self, self.hash))
#        return self.hash


# The current "id" and "pointer" logic means we can't create shapes
# while creating other shapes, shape creation has to be atomic this way

# "Pointer" is what/where TypeId is currently constructing an ID for.

from axi.util import Console

class TypeId():

    # Static variables so we can easily get a new id for an
    # object easily and "painlessly." - think this maybe? like actual "hashing"...

    sketch_id = None
    shape_id = None
    vector_id = None

    sketch_pointer = 0
    shape_pointer = 0
    # vector_pointer = 0
    node_pointer = 0

    creating_sketch = False
    creating_shape = False

    def __repr__(self):
        class_color = "white"
        if self.type == "shape":
            class_color = "orange"
        elif self.type == "node":
            class_color = "cyan"

        cutoff = 14
        hash = "{}{}".format(self.hash, " "*cutoff)

        # if (self.type == "node"):
        #     return "(:{} {})".format(hash[0:cutoff], self.type)

        return "{}{} {}{}{}".format(
            Console.format("(".format(self.type), ["", class_color]),
            Console.format(":{}".format(hash[0:cutoff]), [class_color]),
            Console.format("{} ".format(self.shape_id if self.type == "node" else "_"), ["orange" if self.type == "node" else "gray-1"]),
            Console.format("{}".format(self.type), ["italic", class_color]),
            Console.format(")".format(self.type), ["", class_color]))

    # Not possible if we're using these objects as keys, 
    # so for now a Scheduelr and Generator will use id.hash string as the dict key
    def __eq__(self, id) -> bool:
        if isinstance(id, TypeId):
            return self.hash == id.hash
        return id == self.hash

    @classmethod
    def sketch(cls, name, **kwargs):
        # print("types/id/TypeId.sketch({})".format(name))

        cls.sketch_id = name
        hash = "{}".format(name)

        cls.sketch_pointer += 1
        cls.shape_pointer = 0
        cls.vector_pointer = 0

        cls.shape_id = cls.shape_pointer
        cls.vector_id = cls.vector_pointer

        return cls("sketch", hash, kwargs)

    @classmethod
    def shape(cls, **kwargs):
        # print("types/id/TypeId.shape()")

        cls.shape_id = cls.shape_pointer
        hash = "{}-{}".format(cls.sketch_id, cls.shape_id)

        cls.shape_pointer += 1

        # cls.vector_pointer = 0
        # cls.vector_id = cls.vector_pointer

        return cls("shape", hash, shape_id=cls.shape_id)

    @classmethod
    def node(cls, shape_id):
        # print("types/id/TypeId.node({})".format(shape_id))

        # We call this only between making Shapes and making Sketches
        # cls.shape_pointer and cls.shape_id are currently at the last shape of the Sketch,
        # So we rest the pointer at the start of linked list creation, and increment it
        # in the Shape loop, so a given node has the appropriate shape_id.

        s = "{}-{}-{}".format(cls.node_pointer, cls.sketch_id, shape_id)
        # shape_id = cls.shape_pointer
        cls.node_pointer += 1

        return cls("node", s, shape_id=shape_id)

    # Used because when we ask Generator to create a linked list, the Sketch
    # and Shape creation process left shape_id/shape_pointer at the end of its
    # possible list. So we reset this here so our new linked list Node items point
    # to the proper shape_id
    #@classmethod
    #def reset_shape_pointer(cls):
    #    print("types/id/reset_shape_pointer()")
    #    cls.shape_pointer = 0
    #    cls.shape_id = cls.shape_pointer
    #
    #@classmethod
    #def increment_shape_pointer(cls):
    #    print("types/id/increment_shape_pointer()")
    #    cls.shape_pointer += 1
    #    cls.shape_id = cls.shape_pointer


    def __init__(self, type, hash, shape_id):
        # print("types/id/TypeId.__init__(type={}, hash={}, shape_id={}".format(type, hash, shape_id))
        self.type = type
        self.hash = hash
        # for k in kwargs:
        #     setattr(self, k, kwargs.get(k)) 
        self.shape_id = shape_id
        # print("types/id/TypeId self.__dict__ is now: {}".format(self.__dict__))
