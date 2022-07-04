"""
Invokes base functionality when axi is run as a script.
Example: python3 -m axi -a square -t 100
"""

import argparse
import sys
import textwrap

import signal
from threading import Event
exit_signal = Event()

# https://docs.python.org/3/library/__main__.html
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#python-requires

from .objects import Plotter

VERSION = (0, 0, 1)

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
    print('__main__ -> handle_interrupt(%d)' % s)
    exit_signal.set()


def main() -> int:
    """Connect and talk to Axidraw"""
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
    # parser.add_argument('-p', '--pos', nargs=2, help='xy pos for plotter')
    # parser.add_argument('-a', '--action', help='action for the plotter')
    # parser.add_argument('-t', '--time', default=30, help='min/max time action can take in s', type=int)
    parser.add_argument('-d', '--debug', help='display live debug information, levels of verbosity correspond number of arguments e.g. -ddd', action='count', default=0) #action=FooAction,)
    # parser.add_argument('-v', '--verbose', help='display live debug information', action=FooAction)
    # parser.add_argument('-v', '--version', help='s', action='version', version='%(prog)s %(version)s')
    args = parser.parse_args()
    result = 1;
    plotter = Plotter(args)
    while not exit_signal.is_set():
        plotter.step()
        exit_signal.wait(0.005)
        print('__main__ loop')
    print('__main__ interrupt')
    plotter._disconnect()
        
#    try:
#        loop = Loop(args)
#        result = 0
#    except Exception as e:
#        print('./axi/__main__ exception: %s' % e);        
    return result

sys.exit(main())
