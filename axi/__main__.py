"""
Invokes base functionality when axi is run as a script.
Example: python3 -m axi -a maze -t 100
"""

import argparse
import sys
import textwrap

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

def main() -> int:
    """Connect and talk to Axidraw"""
    # setattr(argparse, 'version', get_version())
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
        epilog='Written by joeysapp'
    )
    parser.add_argument('-a', '--action', help='action for the plotter')
    parser.add_argument('-t', '--time', help='min/max time action can take in s', type=int)
    parser.add_argument('-d', '--debug', help=textwrap.dedent('''
    display live debug information,\n
    levels of verbosity correspond\t\t
    number of arguments e.g. -ddd.
    '''), action='count', default=0) #action=FooAction,)
    # parser.add_argument('-v', '--verbose', help='display live debug information', action=FooAction)
    # parser.add_argument('-v', '--version', help='s', action='version', version='%(prog)s %(version)s')
    args = parser.parse_args()
    result = 1;
    try:
        action = args.action
        time = args.time
        debug = args.debug
        plotter = Plotter(action=action,
                          time_min=time,
                          time_max=time,
                          debug=debug)
        #plotter = Plotter.setup(action=action, time_min=time, time_max=time)
        result = 0
    except Exception as e:
        #print('Error: %s' % e, file=sys.stderr)
        print('./axi/__main__ exception: %s' % e);        
    print("args are: ", args)
    return result

#if __name__ == "__main__":
    # print("./axi/__main__ , name= %s" % __name__)
sys.exit(main())
