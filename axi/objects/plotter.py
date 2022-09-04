from pyaxidraw import axidraw
import asyncio
import time
import math
import random
import time

from axi.util import Console
from axi.math import Vector
from axi.objects import Graph

## Underlying serial connection:
## Users/____/Library/Python/3.8/lib/python/site-package/plotink/ebb_serial.py

## https://axidraw.com/doc/py_api/#functions-interactive
## interactive() 	Initialize Interactive context.
## connect() 	        Open serial connection to AxiDraw.
## disconnect() 	Close serial connection to AxiDraw.
## update() 	        Apply changes to options.
## goto()            	Absolute move to (x,y) location.
## moveto()        	Absolute pen-up move to (x,y) location.
## lineto()        	Absolute pen-down move to (x,y) location.
## go()         	Relative move of distance (Δx,Δy).
## move()         	Relative pen-up move of (Δx,Δy).
## line()       	Relative pen-down move of (Δx,Δy).
## penup()      	Raise the pen.
## pendown()     	Lower the pen.
## current_pos() 	Query machine XY position.
## turtle_pos() 	Query turtle XY position.
## current_pen() 	Query if machine pen state is up.
## turtle_pen() 	Query if turtle pen state is up.

## https://evil-mad.github.io/EggBot/ebb.html

## usb_command() 	Low-level serial command.
## usb_query() 	Low-level serial query.
## step_pos = ad.usb_query("QS\r") # Query step position
## print("Step pos: " + step_pos)
## ad.usb_command("HM,3200\r")     # Return home at 3200 steps/s

# Time to wait before certain commands
plotter_wait = 0.01

class Plotter:
    def __init__(self, args):
        Console.log("Plotter.__init__(args={})\n".format(args))
        self.axidraw = axidraw.AxiDraw()
        self.init()

    # def pause(self):
    # def resume(self):
    # def pause_to_change_pen_position_lol(self):

    def do(self, node):
        Console.log("Plotter.do({})\n".format(node))
        action = node.action
        pos = node.pos
        if (action == "raise"):
            self.axidraw.penup()
        elif (action == "lower"):
            self.axidraw.pendown()
        elif (action == "move"):
            # todo(joeysapp): determine how far we're moving and how long to wait
            self.axidraw.goto(pos.x, pos.y);
        elif (action == "wait"):
            return None

    def check_bounds(self, node, bounds) -> bool:
        return True

    # 1 if up, 0 if down
    def get_pen_state(self) -> int:
        return int(self.axidraw.usb_query('QP\r'))
    
    def get_version(self) -> str:
        return self.axidraw.usb_query('V\r')

    def get_options(self) -> str:
        s = ""
        for k in dir(self.axidraw.options):
            if (k.find('__') == -1):
                s += "{}: {}\n".format(k, getattr(self.axidraw.options, k))            
        return s

    def set_pen_position_range(self):
        self.axidraw.usb_command('SC,4,%i' % self.pen_pos_up)
        self.axidraw.usb_command('SC,5,%i' % self.pen_pos_down)

    def disable_motors(self):
        self.axidraw.usb_command('EM,0,0\r');

    def enable_motors(self):
        self.axidraw.usb_command('EM,1,1\r');

    def init(self):
        try:
            self.axidraw.interactive()
            self.axidraw.connect()
            time.sleep(plotter_wait)
            self.configure();
            Console.log("Plotter.init() -> 0\n")
            return 0
        except Exception as err:
            Console.error("Plotter.init() -> 1 -> {}\n".format(err))
            return err

    def disconnect(self):
        try:
            self.axidraw.penup()
            self.axidraw.goto(0, 0);
            time.sleep(plotter_wait);
            self.axidraw.disconnect()
            Console.log("Plotter.disconnect() -> 0\n")
            return 0
        except Exception as err:
            Console.log("Plotter.disconnect() -> 1 -> {}\n".format(err))
            return err

    def configure(self):
        self.params = {
            "use_b3_out": False,         # enable digital output B3, 3.3V (high) when pen is down, low otherwise
            "clip_to_page": True,        # draw_path(vert_list) handles pen being OOB.. kinda nice..
        }
        self.options = {
            "units": 2,                  # changed -  (in, cm, mm)
            "model": 2,                  # chagged, SE/A3 - https"://axidraw.com/doc/py_api/#model
            "auto_rotate": False,        # changed, if SVG is taller than it is wide, it will print in landscape not portrait
            "pen_pos_down": 50,          # changed, default 40
            "pen_pos_up": 100,           # changed, default 60
            "accel": 75,                 # d, default 75
            "pen_rate_lower": 75,        # d, default 75
            "pen_rate_raise": 50,        # d, default 50
            "pen_delay_down": 0,         # d, default 0 added delay after lowering pen (ms)
            "pen_delay_up": 0,           # d, default 0, delay after raising pen (ms)
            "const_speed": False,        # d, default False option, use constant speed when pen is down
            "speed_pendown": 25,         # d, default 25 - maximum speed while pendown
            "speed_penup": 75,           # d, default 75 - maximum speed while penup
            # "report_time": True # end of plot, throws err?
            # "port":  specify a usb port
            # "port_config": #override how usb portrs are located
            "report_lifts": True,
            "reordering": 0, # 0 1 2 # (default 0, no optimizing)
            "webhook": False, # webhook alerts
            "webhook_url": '',
            "check_updates": False,
            "random_start": False, # randomize start location of closed paths
        }
        # options/params are funny optparse things
        for k in self.params:
            setattr(self.axidraw.params, k, self.params[k])
        for k in self.options:
            #Console.log("1  axi={}    self={}\n".format(getattr(self.axidraw.options, k), self.options[k] or None))
            setattr(self.axidraw.options, k, self.options[k])
            #Console.log("2  axi={}    self={}\n\n".format(getattr(self.axidraw.options, k), self.options[k] or None))
        self.axidraw.update()
        time.sleep(0.5)
        Console.log("Plotter.configure() -> 0 -> \n{}\n".format(self.get_options()))            
        return 0

# params = <module 'axidrawinternal.axidraw_conf' from '/Users/zooey/Library/Python/3.8/lib/python/site-packages/axidrawinternal/axidraw_conf.py'>

# options = {'ids': [], 'selected_nodes': [], 'speed_pendown': 25, 'speed_penup': 75, 'accel': 75, 'pen_pos_down': 30, 'pen_pos_up': 60, 'pen_rate_lower': 50, 'pen_rate_raise': 75, 'pen_delay_down': 0, 'pen_delay_up': 0, 'no_rotate': False, 'const_speed': False, 'report_time': False, 'page_delay': 15, 'preview': False, 'rendering': 3, 'model': 1, 'port_config': 0, 'port': None, 'setup_type': 'align', 'resume_type': 'plot', 'auto_rotate': True, 'random_start': False, 'reordering': 0, 'resolution': 1, 'digest': 0, 'webhook': False, 'webhook_url': None, 'mode': 'interactive', 'submode': 'none', 'manual_cmd': 'fw_version', 'walk_dist': 1, 'layer': 1, 'copies': 1, 'units': 0}
