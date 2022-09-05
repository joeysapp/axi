#!/usr/bin/python3.8
"""

axi module for interacting with Axidraw via serial
$ python3.8 -m axi

"""
VERSION = (0, 3, 0)

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






# Main loop
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



    # 11 x 17in -> 27.94 x 43.18cm -> mm
    # "x" is the vertical axis for plotter
    # "y" is the horiz axis for plotter
    bounds = {
        "min": { "x": 0, "y": 0 },
        "max": { "x": 431.8, "y": 279.4 },
    }

    # Interrupt signal delay - fraction of a second
    loop_delay = 1
    standard_plotter_delay = 1

    scheduler = Scheduler(cli_args)
    # plotter = Plotter(cli_args)
    cmd = None
    head = None
    while not exit_signal.is_set():
        Console.log("[_]\n")
        if (scheduler.head == None):
            Console.info("[A] Scheduler head is None.\n")
            # Are there any generators in the scheduler.queue?
            if (len(scheduler.queue) == 0):
                # No, we don't have anything to print
                Console.info("[AA] Scheduler queue is empty.\n")
                while True:
                    Console.print(".")
                    time.sleep(1)
            else:
                # Yes, last loop a senerator was added to the queue
                Console.info("[AB] Scheduler queue has items.\n")
                next_generator = scheduler.pop_queue()
                # A senerator's id is the first node
                scheduler.head = next_generator.id
                # Add all the new nodes to the scheduler's nodes
                scheduler.nodes.update(next_generator.nodes)
        else:
            Console.info("[B] Scheduler.head exists.\n")

            # Should we look at head.next? If None, next loop goes to A.
            # So add uhhhhhh.. the start of the generator to the scheduler.history?        

            # Can the plotter go to the head?
            if (plotter.check_bounds(head.pos, bounds)):
                Console.info("[BA] Plotter can go to Scheduler.head.\n")
                # Yes, now determine if/what command should be sent to the plotter
                serial_command = scheduler.finite_state_machine(head, head.next)
                # If our FSM action was a transitory state, no serial command needs to send
                if (serial_command == None):
                    Console.info("[BAA] Scheduler.head requires no serial.\n")
                    continue
                else:
                    Console.info("[BAB] Scheduler.head requires serial.\n")
                    plotter.do_command(serial_command)
                    if (serial_command == "move"):
                        # If we're moving, find out if we need to wait after sending the above command.
                        Console.info("[BABA] Scheduler.head to Scheduler.head.next is {} -> {}, ".format(head.pos, head.next.pos))
                        travel_distance = Vector.dist(head.pos, head.next.pos)
                        travel_wait = travel_distance * 10
                        time.sleep(travel_wait)
                        Console.info("dist={travel_distance} wait={travel_wait}\n".format(travel_distance, travel_wait))
                    else:
                        # The action did not require additional waiting [ up, down, raise, lower ]
                        Console.info("[BABB] Scheduler.head is not moving, wait={}\n".format(standard_plotter_delay))
                        time.sleep(standard_plotter_delay)
            else:
                Console.info("[BB] Plotter can not go to Scheduler.head.\n")

                # No.. but are we raised? If we're lowered, should we raise?
                # Prevent pen getting stuck in a down position

                break        

        # todo(@joeysapp on 2022-09-03):
        # - Another thread, listening for user input for cmd
        # # https://stackoverflow.com/questions/4995419/in-python-how-do-i-know-when-a-process-is-finished


        exit_signal.wait(loop_delay)


#        # Old logic
#        # Plotter
#        if (head != None and plotter.check_bounds(head, bounds)):
#            plotter.do(head)
#            graph.extend_history()
#            graph.move_head_to_next_node()
#        # Decide where the plotter is going next
#        if (cmd != None):
#            # User/loaded-in commands
#            gen = generator.do(cmd, head, bounds)
#            graph.add_nodes(gen["nodes"])
#            graph.set_head(gen["id"])
#            cmd = None
#        elif (head.action == 'finish' or head.action == "none"):
#            # do things with previous graph entries: ....
#            # Random:
#            gen = generator.get_random(head, bounds)
#            graph.add_nodes(gen["nodes"])
#            print("WAT", head.action)
#            print("OK!", gen["id"])
#            graph.set_head(gen["id"])
#        head = graph.get_head()

    Console.log("__main__.exit() at {:.2f} seconds\n".format(time.process_time()))
    # plotter.disconnect()
    return std_result

sys.exit(axi())
