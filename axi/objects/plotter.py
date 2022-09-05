from pyaxidraw import axidraw

from axi.util import Console, Timer
from axi.math import Vector
from axi.objects import Graph

## Underlying serial connection:
## - Users/____/Library/Python/3.8/lib/python/site-package/plotink/ebb_serial.py
## Documentation:
## - https://evil-mad.github.io/EggBot/ebb.html

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


## usb_command() 	Low-level serial command.
## usb_query() 	Low-level serial query.
## step_pos = ad.usb_query("QS\r") # Query step position
## print("Step pos: " + step_pos)
## ad.usb_command("HM,3200\r")     # Return home at 3200 steps/s

class Plotter:
    def __init__(self, args):
        Console.log("Plotter.__init__(args={})\n".format(args))
        self.axidraw = axidraw.AxiDraw()
        try:
            self.axidraw.interactive()
            self.axidraw.connect()
            # Next calls to .update(), wait so connection is up
            Timer.wait()
            self.configure();

            Console.log("Plotter.__init__() -> 0\n")
            return 0
        except Exception as err:
            Console.error("Plotter.__init__() -> 1 -> {}\n".format(err))
            return err

    # def pause(self):
    # def resume(self):
    # def pause_to_change_pen_position_lol(self):

    # [ main BAA -> Serial ]
    def do_serial_action(self, action, pos):    
        # action = [ 'up', 'down', 'raise', 'lower', 'move' ]
        # Should only see 'raise' 'lower', and 'move'.
        if (action == 'move' and pos):
            plotter.goto(pos[0], pos[1])
        elif (action == 'raise'):
            plotter.penup()
        elif (action == 'lower'):
            plotter.pendown()
        else:
            Console.error("Plotter.do_serial_action(action={} pos={}) -> !! SHOULD NOT BE CALLED !!".format(action, pos))


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


    def disconnect(self):
        try:
            self.axidraw.penup()
            self.axidraw.goto(0, 0);
            Timer.wait()
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
        for k in self.params:
            setattr(self.axidraw.params, k, self.params[k])
        for k in self.options:
            setattr(self.axidraw.options, k, self.options[k])

        self.axidraw.update()
        Console.log("Plotter.configure() -> 0 -> {}\n".format(self.get_version()))            
        return 0

# params = <module 'axidrawinternal.axidraw_conf' from '/Users/zooey/Library/Python/3.8/lib/python/site-packages/axidrawinternal/axidraw_conf.py'>
