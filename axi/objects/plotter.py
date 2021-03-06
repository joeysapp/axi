from pyaxidraw import axidraw
import asyncio
import time
import math
import random
import time

# from axi.util import Console
from axi.math import Vector
from axi.objects import Path
from axi.util import map

# Users/____/Library/Python/3.8/lib/python/site-package/plotink/ebb_serial.py
# https://stackoverflow.com/questions/4995419/in-python-how-do-i-know-when-a-process-is-finished

class Plotter:
    def __init__(self, args, **kwargs):
        print('objects/plotter/Plotter.__init__')
        for k, v in kwargs.items():
            print("Plotter.__init__: %s == %s" % (k, v))
        self._axidraw = axidraw.AxiDraw()
        self._connect()
        self.min = [Vector(0, 0, 0), Vector(0, 0, 0)]
        self.max = [Vector(100, 200, 0), Vector(100, 200, 0)]
        self.shift_x = 0
        self.shift_y = 0
        self.traversed_path = Path(args)

    # def pause(self):
    # def resume(self):
    # def pauseToChangePenHeight(self):

    # used to traverse a Path
    def path_execute(self, path):
        for path_entry in path.path_entries:
            self._axidraw.goto(pos.x, pos.y)
            self.traversed_path.extend(path_entry)
            time.sleep(0.5)

    def path_extend(self, path_extension):
        self.traversed_path.extend(path_extension)

    # used with iteratively-generated Path items from ./generator.py
    def path_step(self, path_entry, path_idx):
        print('objects/plotter/path_step[%i] : \n\t%s' % (path_idx, str(path_entry)))
        serial_pen_pos = int(self._axidraw.usb_query('QP\r')) # 1 if up, 0 if down

        last_path_entry = self.traversed_path.get(-1)
        last_pen_pos = last_path_entry.pen_pos
        last_pos = last_path_entry.pos

        pos = path_entry.pos
        while (pos.x > self.max[0].x):
            pos.x -= self.max.x[0]
        while (pos.x < self.min[0].x):
            pos.x += self.max[0].x

        while (pos.y > self.max[1].y):
            pos.y -= self.max[1].y
        while (pos.y < self.min[1].y):
            pos.y += self.max[1].y

        d = last_pos.dist(pos);
        print('d: ', d)
        if (d > 10):
            print('wrapped')
            path_entry.pen_pos = 1
            self._axidraw.penup()
            time.sleep(0.5);
        elif (last_pen_pos == 1):
            print('lower')
            path_entry.pen_pos = 0
            self._axidraw.pendown()
            time.sleep(0.5)

        # else if (pen_pos === '0' and not in_bounds): raise
        self._axidraw.goto(pos.x, pos.y)
        # path_entry.pos = pos
        print('extending with: ', path_entry)
        self.traversed_path.extend(path_entry)
        return path_entry.pen_pos

    def _connect(self):
        try:
            self._axidraw.interactive()
            self._axidraw.connect()
            self._configure();
            print('objects/plotter/_connect ok \t %s' % self._axidraw.usb_query('V\r'))
        except Exception as err:
            print('objects/plotter/_connect fail %s', err);
            pass

    def _disconnect(self):
        try:
            print('objects/plotter/_disconnect ok')
            self._axidraw.penup()
            self._axidraw.goto(0, 0);
            time.sleep(0.5);
            self._axidraw.disconnect()
        except Exception as err:
            print('objects/plotter/_disconnect fail %s', err);
            pass
            
    def _disable_motors(self):
        self._axidraw.usb_command('EM,0,0\r');

    def _enable_motors(self):
        self._axidraw.usb_command('EM,1,1\r');

    def setPenBounds(self):
        self._axidraw.usb_command('SC,4,%i' % self.pen_pos_up)
        self._axidraw.usb_command('SC,5,%i' % self.pen_pos_down)

    def _configure(self):
        """ examples_config/axidraw_conf_copy.py """
        print('objects/plotter/_configure');
        self._axidraw.options.pen_pos_down = 0
        self._axidraw.options.pen_pos_up = 75
        #self._axidraw.options.speed_pendown = 25 # maximum speed while pendown
        #self._axidraw.options.speed_penup = 75 # maximum speed while penup

        #self._axidraw.usb_command('SC,4,%i' % self.pen_pos_up)
        #self._axidraw.usb_command('SC,5,%i' % self.pen_pos_down)

        self._axidraw.options.units = 2 # (in, cm, mm)
        self._axidraw.options.model = 2 # https://axidraw.com/doc/py_api/#model
        # self._axidraw.options.report_time = True # end of plot, throws err?
        self._axidraw.options.report_lifts = True 
        self._axidraw.options.auto_rotate = False # (default true)
        self._axidraw.options.reordering = 0 # 0 1 2 # (default 0, no optimizing)
        self._axidraw.params.use_b3_out = False # enable digital output B3, 3.3V (high) when pen is down, low otherwise

        self._axidraw.options.webhook = False # webhook alerts
        self._axidraw.options.webhook_url = '';
        self._axidraw.options.check_updates = False
        self._axidraw.options.random_start = False # randomize start location of closed paths
        self._axidraw.options.accel = 75 
        self._axidraw.options.pen_rate_lower = 75
        self._axidraw.options.pen_rate_raise = 50

        self._axidraw.options.pen_delay_down = 0 # added delay after lowering pen (ms)
        self._axidraw.options.pen_delay_up = 0 # delay after raising pen (ms)
        self._axidraw.options.const_speed = False # option, use constant speed when pen is down
        # self._axidraw.options.port # specify a usb port
        # self._axidraw.options.port_config #override how usb portrs are located
        # self._axidraw.params.clip_to_page # Read "clip_to_page" parameter value

        self._axidraw.update()


## _self.axidraw methods
## https://axidraw.com/doc/py_api/#functions-interactive

## interactive() 	Initialize Interactive context.
## connect() 	Open serial connection to AxiDraw.
## disconnect() 	Close serial connection to AxiDraw.
## update() 	Apply changes to options.
## goto() 	Absolute move to (x,y) location.
## moveto() 	Absolute pen-up move to (x,y) location.
## lineto() 	Absolute pen-down move to (x,y) location.
## go() 	Relative move of distance (??x,??y).
## move() 	Relative pen-up move of (??x,??y).
## line() 	Relative pen-down move of (??x,??y).
## penup() 	Raise the pen.
## pendown() 	Lower the pen.
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
