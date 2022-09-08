import time

from .console import Console

class Timer():
    # Class variables
    default = 1
    dt = 1 # fraction of a second
    
    @classmethod
    def wait(cls, t=None):
        if (t == None):
            t = cls.default
        Console.time("wait for {}\n".format(t))
        time.sleep(t)

    @classmethod
    def get_id(cls):
        t = round(time.time())
        id = "{}".format(str(t))
        Console.time("get_id -> {}\n".format(id))
        return id
