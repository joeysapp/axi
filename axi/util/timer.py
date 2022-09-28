import time

from .console import Console

class Timer():
    default = 0.1
    dt = 0.08 # used in exit loop pausing
    
    @classmethod
    def wait(cls, t=None):
        if (t == None):
            t = cls.default
        Console.time("{}\n".format(t))
        time.sleep(t)
