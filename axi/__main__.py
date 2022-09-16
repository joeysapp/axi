#!/usr/bin/python3.8
"""
tool for interacting with Axidraw
$ python3.8 -m axi

"""
VERSION = (0, 10, 0)

import argparse, sys, textwrap, time, math

from .serial import Serial
from .scheduler import Scheduler
from .generator import Generator
# from .modifier import Modifier

from .util import Console, Timer, fmap
from .types import Vector, Params, ShapeType, v


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
    parser.add_argument('-s', '--do-serial', action='store_true', help='Tells Axi to send serial commands to USB serial connection.')
    parser.add_argument('-l', '--do-lower', action='store_true', help='Tells Axi to lower during plots, otherwise it will never lower.')
    # parser.add_argument('-p', '--pos', nargs=2, help='initial (x y) pos for plotter')
    # parser.add_argument('-d', '--debug', help='display debug info', action='count', default=0)
    args = parser.parse_args()

    scheduler = Scheduler()
    serial = Serial(do_serial=args.do_serial, do_lower=args.do_lower)
    generator = Generator()
    # modifier = Modifier(cli_args)
    # selector = Selector(cli_args)

    thing = generator.create_sketch("foo")

    # for y in range(35, 100, 5):
    #     # thing.add_shape(ShapeType.line, Params(pos=Vector(0, y, 0), length=10, degrees=y/2.0))
    #     for i in range(0, 10, 1):
    #         p = fmap(y, 35, 100, 0, 180) + i/2.0            
    #         p = (p / 180 * math.pi)
    #         thing.add_shape(ShapeType.line, Params(pos=Vector(10, y+(i/2.0), 0), length=10/2.5 + 3.5*math.sin(p), degrees=225))
    # 
    # b1 = thing.get_bounds();
    # vector_000 = thing.get_centroid();

    # for x in range(0, 50, 1):
    #     s = thing.get_shape(type=ShapeType.line, params=Params(pos=Vector(0, 0, 0), legnth = 10, degrees=0))    
    #     s1, s2 = thing.modify_shapes([s], type=Modifier.subdivide, params=Params(count=1))
    #     s3, s4 = thing.modify_shapes([s1, s2], type=Modifier.translate, params=Params(x=0, y=20))        
    #     thing.add_shapes(s1, s2);

    new_nodes, new_head = generator.get_sketch_as_linked_list("foo")
    scheduler.add_nodes(new_nodes)
    scheduler.append_to_queue(new_head)

    loop_count = 0
    while not exit_signal.is_set():
        s = time.perf_counter() * 1
        # Note: process_time () is very different from pref_counter ()
        # because perf_counter ( ) calculates program time with
        # perf_counter () time and if there is any interruption but process_counter
        # only calculates system and CPU time, during process it does not include timeout. 

        Console.info(Console.format("="*80+"\n", ["gray-0"]))
        Console.info("[    ] loop[{}] begin at {} seconds\n".format(loop_count, "{:.3f}".format(s)))
        loop_count += 1

        # [A]
        if (scheduler.head == None):
            Console.info("[A   ] Scheduler head does not exist\n")
            if (len(scheduler.queue) == 0):
                Console.info("[AA  ] There is nothing in Scheduler's queue\n")
                Console.error("[AA  ] Exiting for now\n")
                break;
            else:
                Console.info("[AB  ] Scheduler's queue is populated - will now pop new head from queue and set\n")
                scheduler.pop_queue_to_head()
        # [B]
        elif (scheduler.head != None):
            Console.info("[B   ] Scheduler checks if head.pos is within physical plotter limits")
            # For now, there's a hardcoded check (not even with a ShapeType.rect)
            # Think about the logistics of raising/lowering and Generator.linked_list_creation.
            head_within_bounds = scheduler.is_head_within_physical_bounds()

            if not head_within_bounds:
                # No.. but are we raised? If we're lowered, should we raise?
                # Prevent pen getting stuck in a down position, 
                # maybe for now, USB_query the plotter (only once?) to check if it's up or down
                Console.error("[BB  ] Cannot reach. Breaking loop. todo: think about this logic\n");
                break

            elif head_within_bounds:
                Console.info("[BA  ] Ask the Scheduler if Plotter needs to send a serial command\n")
                command, pos = scheduler.get_serial_command()
                if command != None:
                    Console.info("[BAA ] Serial communication necessary\n")
                    serial.do_serial_command(command, pos)
                    Console.info("[BAA ] Asking Scheduler if the Plotter is moving\n")

                    if (command == "move" or command == "goto"):
                        travel_distance = scheduler.get_travel_distance()

                        # above is in mm units, so distance = 25mm =~ 1 inch, 25/100 means we wait for 0.25 seconds
                        travel_wait = travel_distance / 100.0

                        Console.info("[BAAA] plotter is moving {}mm, waiting for {}s\n".format(travel_distance, travel_wait))
                        Timer.wait(travel_wait)
                    else:
                        Console.info("[BAAB] Plotter is not moving, wait for standard instruction wait\n")
                        Timer.wait()
                else:
                    Console.info("[BAB ] No serial communication\n")
                # H
                Console.info("[B   ] Scheduler now attempts go to head.next\n")
                scheduler.goto_next_node();

        # End of loop
        Console.state("{}\n".format(scheduler))
        Console.info("[    ] loop[{}] end, exit_signal.wait(dt={})\n".format(loop_count, Timer.dt))
        exit_signal.wait(Timer.dt)

    # Exit via exit() or ctrl-c
    Console.log("__main__.exit() at {:.2f} seconds\n".format(time.process_time()))
    serial.disconnect()
    return std_result

sys.exit(axi())
