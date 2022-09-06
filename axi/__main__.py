#!/usr/bin/python3.8
"""
tool for interacting with Axidraw
$ python3.8 -m axi

"""
VERSION = (0, 3, 0)

import argparse, sys, textwrap, time

from .objects import Plotter, Scheduler, Generator
from .util import Console, Timer
from .math import Vector




# note(@joeysapp): this is so C-c won't kill python first before closing the plotter serial connection
import signal
from threading import Event
exit_signal = Event()
def handle_interrupt(signal, _frame):
    Console.error("\n", signal, _frame, "\n");
    std_result = 1
    exit_signal.set()
for s in ('TERM', 'HUP', 'INT'):
    signal.signal(getattr(signal, 'SIG'+s), handle_interrupt);


# - https://docs.python.org/3.8/library/threading.html



std_result = 0
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



    scheduler = Scheduler(cli_args)
    plotter = Plotter(cli_args)


    # If the user passed in an --object arg, generate it here and add it to scheduler.
    # generator = Generator(cli_args)
    sq = Generator(type="square", width=10, height=20, pos=Vector(5, 0, 0))
    # new_nodes, new_head = sq.gen()
    scheduler.push_generator_to_stack(sq)


    # Main loop
    while not exit_signal.is_set():
        Console.info("[    ] begin\n")
        # [A]
        if (scheduler.head == None):
            Console.info("[A   ] Scheduler head does not exist\n")
            # Are there any generators in the scheduler.stack?
            if (len(scheduler.stack) == 0):
                Console.info("[AA  ] There is nothing in the Scheduler stack\n")
                Console.error("[AA  ] Exiting for now\n")
                break;
            else:
                Console.info("[AB  ] Scheduler stack is populated, we pop the Generator and call .gen()\n")
                scheduler.pop_generator_stack()
                Console.log("[AB  ] Scheduler is now: {}\n".format(scheduler))
                # break
        # [B]
        elif (scheduler.head != None):
            Console.info("[B   ] Scheduler head exists and is not null\n")

            # 11 x 17in -> 27.94 x 43.18cm -> mm
            # "x" is the vertical axis for plotter
            # "y" is the horiz axis for plotter
            bounds = {
                "min": { "x": 0, "y": 0 },
                "max": { "x": 431.8, "y": 279.4 },
            }

            # I'm mostly wanting dynamic change this, like, "I cannot print outside this tiny circle" kinda thing
            head_within_bounds = scheduler.is_head_within_bounds(bounds)
            if not head_within_bounds:
                Console.info("[BB  ] Scheduler head is out of bounds: {}\n".format(bounds))
                Console.err("[BB  ] Break loop for now\n");
                # No.. but are we raised? If we're lowered, should we raise?
                # Prevent pen getting stuck in a down position, 
                # maybe for now, USB_query the plotter (only once?) to check if it's up or down

                break
            elif head_within_bounds:
                Console.info("[BA  ] Scheduler head is within bounds: {}\n".format(bounds))

                # Handling our various pen states to prevent redundant serial calls to plotter
                # All the plotters needs is: (action [position])
                command, pos = scheduler.get_serial_command_for_plotter()
                Console.info("[BA  ] Ask the scheduler what, if anything, should be sent over serial\n")

                if (command == None):
                    Console.info("[BAB ] No serial commnication necessary\n".format(command, pos))
                else:
                    Console.info("[BAB ] Serial communication necessary\n".format(command, pos))
                    plotter.do_serial_command(command, pos)
                    Console.info("[BAB ] Asking Scheduler if the Plotter is moving\n".format(command, pos))
                    if (command == "move"):

                        # If we're moving, find out if we need to wait
                        travel_distance = scheduler.get_travel_distance()
                        travel_wait = travel_distance * 0
                        Console.info("[BAAA] It is moving {travel_distance} and now wait for {travel_wait}\n".format(travel_distance, travel_wait))
                        Timer.wait(travel_wait)

                    else:
                        # The command did not require additional waiting [ up, down, raise, lower ]
                        Console.info("[BAAB] Plotter is not moving\n")
                        Timer.wait()

        Console.info("\n")
        Console.info("[    ] end\n")

        # H
        Console.info("[H   ] Scheduler now attempts go to head.next\n")
        if (scheduler.head):
            Console.info("[H   ] {}\n".format(scheduler.head))            
            scheduler.traverse_linked_list();        
            Console.info("[H   ] {}\n\n\n\n\n\n\n".format(scheduler.head))
        else:
            Console.info("[H   ] scheduler.head is None\n")

        # todo(@joeysapp on 2022-09-03):
        # - Another thread, listening for user input for cmd
        # # https://stackoverflow.com/questions/4995419/in-python-how-do-i-know-when-a-process-is-finished

        
        exit_signal.wait(Timer.loop_delta) # Interrupt signal delay - fraction of a second

    Console.log("__main__.exit() at {:.2f} seconds\n".format(time.process_time()))
    plotter.disconnect()
    return std_result

sys.exit(axi())
