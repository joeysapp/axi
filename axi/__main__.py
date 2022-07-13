"""
Invokes base functionality when axi is run as a script.
Example: python3 -m axi -a square -t 100
"""

import argparse
import sys
import textwrap
import time

import signal
from threading import Event
exit_signal = Event()

# https://docs.python.org/3/library/__main__.html
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#python-requires

from .objects import Plotter
from .objects import Path, PathEntry
from .objects import Generator

from .math import Vector


VERSION = (0, 0, 2)

def get_version() -> str:
    v = '%i.%i.%i' % VERSION
    return v

class FooAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        print("rawr", option_strings, nargs, kwargs)
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print("RAWR", option_strings, nargs, kwargs)        
        print('\n\n%r %r %r' % (namespace, values, option_string))
        setattr(namespace, self.dest, values)

def handle_interrupt(s, _frame):
    print('\n\n__main__->handle_interrupt(%s)' % s)
    exit_signal.set()

def main() -> int:
    """Connect and talk to Axidraw"""
    result = 1;
    # safely disconnect from axidraw and send it to 0,0 on ctrl-c
    for s in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+s), handle_interrupt);
    parser = argparse.ArgumentParser(
        prog='axi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
        axi (%s)
        ----------------------------
            This is a python module that can be
            ran as a script to connect to a local
            or remote axidraw and control it.

            Featuring safe connections and the
            ability to prevent axidraw interrupts
            or otherwise sketch-breaking events.
        ''' % get_version()),
        epilog='Written by @joeysapp'
    )
    parser.add_argument('-p', '--pos', nargs=2, help='initial (x y) pos for plotter')
    parser.add_argument('-b', '--bounds', nargs=4, help='bounds relative to pos, xmin ymin xmax ymax')
    parser.add_argument('-d', '--debug', help='display debug info', action='count', default=0)
    cli_args = parser.parse_args()

    # gen adds to path, using internal actions such as:
    # Shapes
    ## Square(xpos ypos xlength ylength rotation)
    ## Circle(xpos hpos radius sides)      # sides=3 is triangle
    gen = Generator(cli_args)
    path = Path(cli_args, initial_path_entry=start);
    plotter = Plotter(cli_args)

    path_idx = 0
    loop_delay = 0.0005
    while not exit_signal.is_set():

        print('\n\n\n__main__ loop(%i / %i)' % (path_idx, path.length))
        if (path_idx >= 
        current_path_entry = path.get(path_idx)
        print('000 ', end='')
        next_path_entry = gen.next(path_entry=current_path_entry)
        print('001 ', end='')
        next_pen_pos = plotter.path_step(current_path_entry, path_idx)
        next_path_entry.pen_pos = next_pen_pos
        path.extend(next_path_entry)

        # gen.set_options();

        path_idx += 1
        exit_signal.wait(loop_delay)
    print('__main__ exit(t=%f)' % time.process_time())
    plotter._disconnect()
    # path.save()
    return result

sys.exit(main())
