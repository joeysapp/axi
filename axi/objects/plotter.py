from pyaxidraw import axidraw
import asyncio

from axi.util import Console
from axi.math import Vector

class Plotter:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            print("Plotter.__init__: %s == %s" % (k, v))

        self.axidraw = axidraw.AxiDraw();
        self.head = Vector(position=[0, 0])
        self.path = []
        self.log = Console()

    def connect(self):
        try:
            self.axidraw.interactive()
            self.axidraw.connect()
        except Exception:
            print("failed to connect", Exception);
            pass

    def disconnect(self):
        try:
            self.axidraw.disconnect()
        except Exception:
            print("failed to disconnect", Exception);
            pass
            

# from pyaxidraw import axidraw   # import module
# ad = axidraw.AxiDraw()          # Initialize class
# ad.interactive()                # Enter interactive context
# ad.options.pen_pos_up = 70      # set pen-up position
# ad.connect()                    # Open serial port to AxiDraw 
# ad.moveto(1,1)                  # Absolute pen-up move, to (1 inch, 1 inch)
# ad.lineto(0,0)                  # Absolute pen-down move, back to origin.
# ad.disconnect()                 # Close serial port to AxiDraw

#    https://github.com/django/django/blob/main/django/apps/config.py
#    def __repr__(self):
#        return "<%s: %s>" % (self.__class__.__name__, self.label)
#  
#    @cached_property
#    def default_auto_field(self):
#        from django.conf import settings
#  
#        return settings.DEFAULT_AUTO_FIELD
#  
#    @property
#    def _is_default_auto_field_overridden(self):
#        return self.__class__.default_auto_field is not AppConfig.default_auto_field
