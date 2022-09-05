import time

from .console import Console

class Timer():
    # Class variables
    default = 1
    loop_delta = 2 # fraction of a second
    
    @classmethod
    def wait(cls, t=None):
        if (t == None):
            t = cls.default
        Console.info("[timer] wait for {}\n".format(t))
        time.sleep(t)
