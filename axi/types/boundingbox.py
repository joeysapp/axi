"""
   BoundingBox objects are referenced in the Scheduler and Sketches.
   .... for now
"""

from .vector import Vector

class BoundingBox():
    # SE/A3 sizes: 11 x 17in -> 27.94 x 43.18cm -> mm
    # "x is the vertical axis for plotter
    # "y is the horiz axis for plotter
    # plotter_physical_max = Vector(431.8, 279.4 },
    # plotter_physical_min = Vector(0, 0)

    def __init__(self, bmin, bmax):
        self.bmin = bmin if bmin else Vector(0, 0)
        self.bmax = bmax if bmax else Vector(431.8, 279.4)

    def check(self, v):
        return v.x > self.min.x and \
               v.y > self.min.y and \
               v.x < self.max.x and \
               v.y < self.max.y
