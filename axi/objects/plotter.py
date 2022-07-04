from pyaxidraw import axidraw
import asyncio
import time
import math
import random
import time

# from axi.util import Console
from axi.math import Vector
from axi.util import map

# https://stackoverflow.com/questions/4995419/in-python-how-do-i-know-when-a-process-is-finished

class Plotter:
    def __init__(self, args, **kwargs):
        print('Plotter.__init__')
        for k, v in kwargs.items():
            print("Plotter.__init__: %s == %s" % (k, v))
        self._axidraw = axidraw.AxiDraw()
        self._connect()
        self.d = False
        self.h = 0
        self.p = [{ 'x': 0, 'y': 0, 'z': 0, 't': 0, 'd': 0}]
        self.b = { 'x': 0, 'X': 100, 'y': 0, 'Y': 100 } # def get_bounds_interactive()
        # self.log = Console()

    # def pause(self):
    # def resume(self):
    # def pauseToChangePenHeight(self):

    def info(self):
        try:
            p = self.p[self.h]
            return 'info() %i (%f %f %f %f %i))' % (self.h, p['x'], p['y'], p['z'], p['t'], p['d'])
        except Exception as e:
            return e

    def info_set(self):
        return None
    
#    def goto(self, p):
#        if (p['x'] > self.b['x'] and p['x'] < self.b['X'] and p['y'] > self.b['y'] and p['y'] < self.b['Y']):
#            self._axidraw.goto(p['x'], p['y'])

    # here's the creative bit
    def get_next(self):
        p = self.p[self.h]
        t = p['t'] % math.pi
        v = map(t, 0, math.pi, -math.pi, math.pi)
        #v = (time.process_time()*500.0)
        
        r = 5
        nx = 25 + r*math.cos(v);
        ny = 25 + r*math.sin(v);
        if (nx > self.b['X'] or nx < self.b['x']):
            self._axidraw.penup()
            nx = random.randrange(self.b['x'], self.b['X']);
        if (ny > self.b['Y'] or ny < self.b['y']):
            ny = random.randrange(self.b['y'], self.b['Y']);
            #ny = self.b[1][1]
            #self._axidraw.penup()
        print('\tget_next[%s]' % (self.info()))
        t = time.process_time()
        self.p.append({ 'x': nx, 'y': ny, 'z': 0, 't': t, 'd': 0 })

    def step(self):
        self.get_next()
        p = self.p[self.h]
        if (p['x'] > self.b['x'] and p['x'] < self.b['X'] and p['y'] > self.b['y'] and p['y'] < self.b['Y']):
            self._axidraw.goto(p['x'], p['y'])
        self.h = self.h + 1
        # print('step', self.h, self.p[self.h])

    def _connect(self):
        try:
            print( )
            self._axidraw.interactive()
            self._axidraw.connect()
            self._configure();
            print('objects/plotter/_connect \t %s' % self._axidraw.usb_query('V\r'))
        except Exception as err:
            print("failed to connect", err);
            pass

    def _disconnect(self):
        try:
            print('objects/plotter/_disconnect')
            self._axidraw.penup()
            self._axidraw.goto(0, 0);
            time.sleep(0.5);
            self._axidraw.disconnect()
        except Exception as err:
            print("failed to disconnect", err);
            pass
            
    def _disable_motors(self):
        self._axidraw.usb_command('EM,0,0\r');

    def _enable_motors(self):
        self._axidraw.usb_command('EM,1,1\r');
                 
    def _configure(self):
        """ examples_config/axidraw_conf_copy.py """
        print('objects/plotter/_configure');
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
        self._axidraw.options.speed_pendown = 25 # maximum speed while pendown
        self._axidraw.options.speed_penup = 75 # maximum speed while penup
        self._axidraw.options.accel = 75 
        #self._axidraw.options.pen_pos_down = 50
        #self._axidraw.options.pen_pos_up = 0
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
## go() 	Relative move of distance (Δx,Δy).
## move() 	Relative pen-up move of (Δx,Δy).
## line() 	Relative pen-down move of (Δx,Δy).
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
