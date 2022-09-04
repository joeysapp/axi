#!/usr/bin/python3.8
"""
Invokes base functionality when axi is run as a script.
Example: python3.8 -m axi -a square -t 100
"""
VERSION = (0, 1, 0)

import argparse, sys, textwrap, time, os
from .objects import Plotter, Graph, Node, Generator
from .util import Console

# note(@joeysapp): Ctrl-c won't break the serial connection
# - https://docs.python.org/3.8/library/threading.html
import signal
from threading import Event
exit_signal = Event()
def handle_interrupt(signal, _frame):
    Console.error("\n", signal, _frame, "\n");
    std_result = 0
    exit_signal.set()
for s in ('TERM', 'HUP', 'INT'):
    signal.signal(getattr(signal, 'SIG'+s), handle_interrupt);





std_result = 1
def axi() -> int:
    parser = argparse.ArgumentParser(
        prog="axi",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
        axi {}
        ----------------------------
            This is a python module that can be
            ran as a script to connect to a local
            or remote axidraw and control it.
        '''.format("%i.%i.%i".format(VERSION[0], VERSION[1], VERSION[2]))),
        epilog="Written by @joeysapp"
    )
    parser.add_argument('-p', '--pos', nargs=2, help='initial (x y) pos for plotter')
    parser.add_argument('-b', '--bounds', nargs=4, help='bounds relative to pos, xmin ymin xmax ymax')
    parser.add_argument('-d', '--debug', help='display debug info', action='count', default=0)
    cli_args = parser.parse_args()

    generator = Generator(cli_args)
    graph = Graph(cli_args);
    plotter = Plotter(cli_args)

    cmd = None
    cmd = "(goto 20 20)"
        # cmd = "(square (0 0) 10 10)"
        # cmd = "(circle (0 0) radius=50 sides=3)"
        # cmd = "(goto 20 20)"

    # Graph "head", where the plotter will try to go next
    head = None

    # Used for generator and bounds checking for Plotter
    bounds = [[0, 0], [279.4, 431.8]] # 11 x 17in -> 27.94 x 43.18cm -> mm

    # Interrupt signal delay - fraction of a second
    loop_delay = 0.5

    while not exit_signal.is_set():
        Console.log("__main__.loop\n")
        
        # todo(@joeysapp on 2022-09-03):
        # - Another thread, listening for user input for cmd
        # # https://stackoverflow.com/questions/4995419/in-python-how-do-i-know-when-a-process-is-finished

        if (cmd != None):
            new_nodes = generator.do(cmd, head, bounds)
            graph.add_nodes(new_nodes)
            cmd = None

        if (head != None and plotter.check_bounds(head, bounds)):
            plotter.do(head)

            graph.extend_history()
            graph.move_head_to_next_node()

        head = graph.get_head()

        exit_signal.wait(loop_delay)

    Console.log("__main__.exit() at {:.2f} seconds\n".format(time.process_time()))
    Console.log("graph: {}".format(graph))
    plotter.disconnect()
    return std_result

sys.exit(axi())
