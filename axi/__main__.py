#!/usr/bin/python3.8
"""
tool for interacting with Axidraw
$ python3.8 -m axi

"""
VERSION = (0, 3, 0)

import argparse, sys, textwrap, time

from .objects import Plotter, Graph, Node, Generator
from .util import Console



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

    # Main loop
    while not exit_signal.is_set():
        Console.log("[_]\n")

        # [A]
        if (scheduler.head == None):
            Console.info("[A_] scheduler.head == None.\n")

            # Are there any generators in the scheduler.stack?
            if (len(scheduler.stack) == 0):
                Console.info("[AA] Nothing in scheduler stack to print.")
                while True:
                    Console.print(".")
                    Timer.wait(1)
            else:
                Console.info("[AB] Scheduler stack contains item; next loop begin printing\n")

                generator = scheduler.stack.pop()

                # Add all the new nodes to the scheduler's nodes                
                scheduler.nodes.update(generator.nodes)
                scheduler.history.append(generator.id)

                # A senerator's id is the first node
                scheduler.head = scheduler.nodes[next_generator.id]
        # [B]
        else:
            Console.info("[B___] scheduler.head exists,\n")

            # Bounds checking outside of plotter now..
            head_within_bounds = True
            # Maybe should go within Scheduler, or perhaps within a Generator itself?
            # I'm mostly wanting dynamic like, "I cannot print outside this tiny circle" kinda thing

            # 11 x 17in -> 27.94 x 43.18cm -> mm
            # "x" is the vertical axis for plotter
            # "y" is the horiz axis for plotter
            bounds = {
                "min": { "x": 0, "y": 0 },
                "max": { "x": 431.8, "y": 279.4 },
            }

            p = head.pos
            if (p.x <= bounds["min"]["x"] or p.x >= bounds["max"]["x"]):
                head_within_bounds = False
            if (p.y <= bounds["min"]["y"] or p.y >= bounds["max"]["y"]):
                head_within_bounds = False

            if not head_within_bounds:
                Console.info("[BB__] plotter cannot go to scheduler.head.\n")

                # No.. but are we raised? If we're lowered, should we raise?
                # Prevent pen getting stuck in a down position, 
                # maybe for now, USB_query the plotter (only once?) to check if it's up or down

                break
            elif head_within_bounds):
                Console.info("[BA__] plotter can go to scheduler.head; scheduler.head={} -> scheduler.head.next={}\n".format(head.state, hext.next.state)))

                # Handling our various pen states to prevent redundant serial calls to plotter
                # All the plotters needs is: (action [position])
                action, pos = scheduler.get_serial_action(head, head.next)


                if (serial_action == None):
                    Console.info("[BAB_] (action={action} pos={pos}) = no serial\n".format(action, pos)))
                    continue
                else:
                    Console.info("[BAB_] (action={action} pos={pos}) = requires serial connection\n".format(action, pos)))


                    # [ BAA -> Serial ]
                    #plotter.do_command(serial_command)

                    if (serial_action == "move"):

                        # If we're moving, find out if we need to wait after sending the above command.
                        Console.info("[BAAA] scheduler.head to scheduler.head.next is {} -> {}, ".format(head.pos, head.next.pos))
                        travel_distance = Vector.dist(head.pos, head.next.pos)
                        travel_wait = travel_distance * 10
                        Timer.wait(travel_wait)

                        Console.info("distance is ={travel_distance} wait={travel_wait}\n".format(travel_distance, travel_wait))
                    else:
                        # The action did not require additional waiting [ up, down, raise, lower ]
                        Console.info("[BAAB] standard wait time, wait={}\n".format(Timer.default))
                        Timer.wait()

        # H
        # Scheduler traverses its linked list
        Console.info("[H] scheduler.head = scheduler.head.next\n")
        Console.info("[H] {} -> ".format(scheduler.head))
        scheduler.head = s.nodes[scheduler.head.next];
        Console.info("{}\n".format(scheduler.head))

        # todo(@joeysapp on 2022-09-03):
        # - Another thread, listening for user input for cmd
        # # https://stackoverflow.com/questions/4995419/in-python-how-do-i-know-when-a-process-is-finished


        exit_signal.wait(Timer.loop) # Interrupt signal delay - fraction of a second



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
    plotter.disconnect()
    return std_result

sys.exit(axi())
