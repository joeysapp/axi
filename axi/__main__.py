#!/usr/bin/python3.8
"""
tool for interacting with Axidraw
$ python3.8 -m axi

"""
VERSION = (0, 9, 0)

import argparse, sys, textwrap, time, math

#from . import Serial, Scheduler, Generator, Modifier
from .serial import Serial
from .scheduler import Scheduler
from .generator import Generator
from .modifier import Modifier

from .util import Console, Timer, fmap
from .types import Vector, Params, ShapeType


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
    serial = Serial(cli_args)
    generator = Generator(cli_args)
    # modifier = Modifier(cli_args)
    # selector = Selector(cli_args)


    # Console.info("Initial setup of Serial, Generator and Scheduler complete\n");
    # Console.info(Console.format("="*80+"\n", ["gray-0"]))
    # Console.info("\n")

    thing = generator.create_sketch("foOO")

    # Playing around
    deg = 5
    l = 10
    for x in range(50, 75, 12):
        for y in range(70, 111, 20):
            deg = 3
            for i in range(0, 360+deg+1, deg):
                xamt = fmap(x, 20, 81, -3, -1)
                yamt = fmap(y, 70, 106, 1, 3) 
                freq = 4
                # 30 frequency means in a full circle, you see a wave every 10 degrees
                length = max(0 + (abs(xamt + yamt))*(1 + math.sin((i / 180) * freq * math.pi))*3, 1)
                # print(x, y, (1 + math.sin((i/ 180) * freq* math.pi)), length)
                lx = length*(math.cos((i / 180) * math.pi))
                ly = length*(math.sin((i / 180) * math.pi))
                px = x + lx
                py = y + ly
                print(i, x, y, '-> ', lx, ly)
                pos = Vector(x, y)
                
            #print("a\n\n")
                thing.add_shape(type=ShapeType.line, params=Params(pos=pos, length=length, degrees=i))
                
        # thing.add_shape(type=ShapeType.line, params=Params(pos=Vector(0, 0, 0), length=10, degrees=45))



    # thing.add_shape(type=ShapeType.line, params=Params(pos=Vector(25, 25, 0), length=5, degrees=225))
    
    new_nodes, new_head = generator.get_sketch_as_linked_list("foOO")
    
    scheduler.add_nodes(new_nodes)
    scheduler.append_to_queue(new_head)

    # Console.info("="*70+"\n")
    # todo(@joeysapp on 2022-09-03):
    # - Another thread, listening for user input for cmd
    # # https://stackoverflow.com/questions/4995419/in-python-how-do-i-know-when-a-process-is-finished   
    
    # Main loop
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
            # Are there any generators in the scheduler stack?
            if (len(scheduler.queue) == 0):
                Console.info("[AA  ] There is nothing in Scheduler's queue\n")
                Console.error("[AA  ] Exiting for now\n")
                break;
            else:
                Console.info("[AB  ] Scheduler's queue is populated - will now pop new head from queue and set\n")
                scheduler.pop_queue_to_head()
                # Console.info("[AB  ] exit now because the serial is turned off and I'm nervous\n")
                # exit()
        # [B]
        elif (scheduler.head != None):
            Console.info("[B   ] scheduler.head = "+
                         Console.format(str(scheduler.head)+"\n", ["white"]))
            Console.info("[B   ] Scheduler checks bounds.. (move this to Generator?)\n")

            # I think ideally we shouldn't have to do this check in the Scheduler..
            # Shouldn't the Generator handle that?
            head_within_bounds = scheduler.is_head_within_bounds()
            if not head_within_bounds:
                Console.info("[BB  ] Scheduler head is out of bounds\n")
                Console.error("[BB  ] Break loop for now, todo: think about this logic\n");
                # No.. but are we raised? If we're lowered, should we raise?
                # Prevent pen getting stuck in a down position, 
                # maybe for now, USB_query the plotter (only once?) to check if it's up or down
                break
            elif head_within_bounds:
                # Handling our various pen states to prevent redundant serial calls to plotter
                # All the plotters needs is: (action [position])
                Console.info("[BA  ] Ask the Scheduler if Plotter needs to send a serial command\n")
                command, pos = scheduler.get_serial_command()

                # if (command == None):
                #    Console.info("[BAB ] No serial commnication necessary\n".format(command, pos))
                if not command == None:
                    Console.info("[BAA ] Serial communication necessary\n")
                    serial.do_serial_command(command, pos)

                    Console.info("[BAA ] Asking Scheduler if the Plotter is moving\n")
                    if (command == "move" or command == "goto"):
                        # If we're moving, find out if we need to wait
                        travel_distance = scheduler.get_travel_distance()
                        # above is in mm units, so distance = 25mm = 1 inch? wait 1 second.
                        travel_wait = travel_distance / 100.0
                        Console.info("[BAAA] plotter is moving {}mm -> wait for {}s\n".format(travel_distance, travel_wait))
                        Timer.wait(travel_wait)
                    else:
                        # The command did not require additional waiting [ up, down, raise, lower ]
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
